import os
import shutil
import psycopg2
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings

__version__ = "0.1.0"

logger = setup_logging(
    "strategy-marketplace",
    log_path="logs/strategy-marketplace/marketplace.log",
    remote_url=settings.remote_log_url,
)
REQUEST_COUNT = setup_metrics(
    "strategy-marketplace", port=settings.strategy_marketplace_metrics_port
)
tracer = setup_tracer("strategy-marketplace")

app = FastAPI(title="strategy-marketplace", version=__version__)

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")


class StrategyIn(BaseModel):
    name: str
    description: str | None = None


class StrategyOut(StrategyIn):
    id: int
    file_path: str


class ReviewIn(BaseModel):
    rating: int
    comment: str | None = None


def get_conn():
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    )


@app.post("/strategies", response_model=StrategyOut)
def create_strategy(data: StrategyIn, file: UploadFile = File(...)):
    with tracer.start_as_current_span("create-strategy"):
        os.makedirs(ASSET_DIR, exist_ok=True)
        file_path = os.path.join(ASSET_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO strategies (name, description, file_path) VALUES (%s,%s,%s) RETURNING id",
                    (data.name, data.description, file_path),
                )
                strategy_id = cur.fetchone()[0]
        conn.close()
        logger.info("Created strategy", extra={"id": strategy_id})
        REQUEST_COUNT.inc()
        return StrategyOut(id=strategy_id, file_path=file_path, **data.dict())


@app.get("/strategies/{strategy_id}", response_model=StrategyOut)
def get_strategy(strategy_id: int):
    with tracer.start_as_current_span("get-strategy"):
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id,name,description,file_path FROM strategies WHERE id=%s",
                    (strategy_id,),
                )
                row = cur.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Strategy not found")
        REQUEST_COUNT.inc()
        return StrategyOut(id=row[0], name=row[1], description=row[2], file_path=row[3])


@app.put("/strategies/{strategy_id}", response_model=StrategyOut)
def update_strategy(strategy_id: int, data: StrategyIn):
    with tracer.start_as_current_span("update-strategy"):
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE strategies SET name=%s, description=%s WHERE id=%s RETURNING file_path",
                    (data.name, data.description, strategy_id),
                )
                res = cur.fetchone()
        conn.close()
        if not res:
            raise HTTPException(status_code=404, detail="Strategy not found")
        logger.info("Updated strategy", extra={"id": strategy_id})
        REQUEST_COUNT.inc()
        return StrategyOut(id=strategy_id, file_path=res[0], **data.dict())


@app.delete("/strategies/{strategy_id}")
def delete_strategy(strategy_id: int):
    with tracer.start_as_current_span("delete-strategy"):
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM strategies WHERE id=%s RETURNING file_path",
                    (strategy_id,),
                )
                res = cur.fetchone()
        conn.close()
        if not res:
            raise HTTPException(status_code=404, detail="Strategy not found")
        file_path = res[0]
        if os.path.exists(file_path):
            os.remove(file_path)
        logger.info("Deleted strategy", extra={"id": strategy_id})
        REQUEST_COUNT.inc()
        return {"status": "deleted"}


@app.post("/strategies/{strategy_id}/reviews")
def create_review(strategy_id: int, review: ReviewIn):
    with tracer.start_as_current_span("create-review"):
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO strategy_reviews (strategy_id, rating, comment) VALUES (%s,%s,%s)",
                    (strategy_id, review.rating, review.comment),
                )
        conn.close()
        logger.info("Added review", extra={"strategy_id": strategy_id})
        REQUEST_COUNT.inc()
        return {"status": "created"}


@app.get("/strategies/{strategy_id}/reviews")
def list_reviews(strategy_id: int):
    with tracer.start_as_current_span("list-reviews"):
        conn = get_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT rating, comment, created_at FROM strategy_reviews WHERE strategy_id=%s",
                    (strategy_id,),
                )
                reviews = [
                    {"rating": r[0], "comment": r[1], "created_at": r[2].isoformat()} for r in cur.fetchall()
                ]
        conn.close()
        REQUEST_COUNT.inc()
        return {"reviews": reviews}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("STRATEGY_MARKETPLACE_HOST", "127.0.0.1")
    port = int(os.getenv("STRATEGY_MARKETPLACE_PORT", "8000"))
    uvicorn.run("strategy-marketplace.api:app", host=host, port=port)

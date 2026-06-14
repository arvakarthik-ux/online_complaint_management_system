from sqlalchemy import func

def complaint_stats(query):
    # Return dict for charts: counts by status and by priority
    by_status = dict(query.session.query(query.column_descriptions[0]['entity'].status, func.count())
                     .select_from(query.subquery())
                     .group_by("status").all())
    # Simpler: run again directly on base model using same filters:
    # But we already have base query; compute by priority too
    # Reuse query to avoid duplicating filters
    subq = query.subquery()
    rows_status = query.session.query(subq.c.status, func.count()).group_by(subq.c.status).all()
    rows_priority = query.session.query(subq.c.priority, func.count()).group_by(subq.c.priority).all()
    return {
        "by_status": {r[0]: r[1] for r in rows_status},
        "by_priority": {r[0]: r[1] for r in rows_priority}
    }

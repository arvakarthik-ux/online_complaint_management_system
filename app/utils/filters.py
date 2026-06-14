from datetime import datetime

def register_template_filters(app):
    @app.template_filter("dt")
    def format_dt(value):
        if not value:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M")
        try:
            return str(value)
        except Exception:
            return ""

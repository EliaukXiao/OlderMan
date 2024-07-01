def init_routes(app):
    from .oldperson_routes import oldperson_bp
    from .employee_routes import employee_bp
    from .volunteer_routes import volunteer_bp
    from .event_routes import event_bp
    from .admin_routes import admin_bp

    app.register_blueprint(oldperson_bp, url_prefix='/api/oldperson')
    app.register_blueprint(employee_bp, url_prefix='/api/employee')
    app.register_blueprint(volunteer_bp, url_prefix='/api/volunteer')
    app.register_blueprint(event_bp, url_prefix='/api/event')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

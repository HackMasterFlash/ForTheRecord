
def create_module(app, **kwargs):
    from .controllers import media_blueprint
    app.register_blueprint(media_blueprint)

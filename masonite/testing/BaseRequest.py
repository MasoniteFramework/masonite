class BaseRequest:
    def user(self, obj):
        self._user = obj
        self.container.on_resolve('Request', self._bind_user_to_request)
        wsgi = generate_wsgi()
        wsgi['PATH_INFO'] = self.url
        self._run_container(wsgi)

        return self

    def ok(self):
        return self.status('200 OK')

    def status(self, value=None):
        if not value:
            return self.container.make('Request').get_status_code()

        return self.container.make('Request').get_status_code() == value

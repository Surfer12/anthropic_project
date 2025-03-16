Traceback (most recent call last):
  File "/Users/ryanoates/anthropic_project/anthropic_client/kob-fourfive.py", line 15, in <module>
    response = client.responses.create(
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/openai/_utils/_utils.py", line 279, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/openai/resources/responses/responses.py", line 602, in create
    return self._post(
           ^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/openai/_base_client.py", line 1242, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/openai/_base_client.py", line 919, in request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/openai/_base_client.py", line 955, in _request
    response = self._client.send(
               ^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpx/_client.py", line 914, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpx/_client.py", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpx/_client.py", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpx/_client.py", line 1014, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpx/_transports/default.py", line 250, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_sync/connection_pool.py", line 256, in handle_request
    raise exc from None
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_sync/connection_pool.py", line 236, in handle_request
    response = connection.handle_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_sync/connection.py", line 103, in handle_request
    return self._connection.handle_request(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_sync/http11.py", line 136, in handle_request
    raise exc
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_sync/http11.py", line 106, in handle_request
    ) = self._receive_response_headers(**kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_sync/http11.py", line 177, in _receive_response_headers
    event = self._receive_event(timeout=timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_sync/http11.py", line 217, in _receive_event
    data = self._network_stream.read(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/site-packages/httpcore/_backends/sync.py", line 128, in read
    return self._sock.recv(max_bytes)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/ssl.py", line 1232, in recv
    return self.read(buflen)
           ^^^^^^^^^^^^^^^^^
  File "/Users/ryanoates/anthropic_project/.magic/envs/default/lib/python3.12/ssl.py", line 1105, in read
    return self._sslobj.read(len)
           ^^^^^^^^^^^^^^^^^^^^^^
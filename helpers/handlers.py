# from flask imports request, g


def before_request_handler():
    # print('hello world')
    # request.hello = 'bye'
    # g.start_time = 'this is the value'
    return


def after_request_handler(response):
    # print(f'bye world {g.start_time}')
    # print(request.hello)
    return response

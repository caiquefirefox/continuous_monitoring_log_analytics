import time
import opentracing
from jaeger_client import Config

def init_jaeger_tracer(service_name='my_service'):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()

if __name__ == "__main__":
    tracer = init_jaeger_tracer()
    with tracer.start_span('test_span') as span:
        span.set_tag('example_tag', 'test_value')
        span.log_kv({'event': 'test_message', 'life': 42})
        time.sleep(1)
    tracer.close()


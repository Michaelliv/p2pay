import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt="%m-%d %H:%M",
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)


def get_logger(namespace: str) -> logging.Logger:
    return logging.getLogger(namespace)

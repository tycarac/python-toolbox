import logging
import pytest


from toolbox.encoder import CharSetEncoder

_logger = logging.getLogger(__name__)


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('', '0fh43w'),
    ('1', 'jtvky4'),
    ('2', '0s5mgf'),
    ('https://docs.aws.amazon.com', 'zfv3pv2'),
    ('https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html/serverless-application-model-updates.rss', '6wdkr6')
    ])
def test_hash(given, expected):
    encoder = CharSetEncoder()
    assert encoder.hash(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    ('', '3vkzzbpyxf'),
    ('1', 'fnkt2wfzg'),
    ('2', '4rvs04xqg9'),
    ('https://docs.aws.amazon.com', 'jzmjqfmdc'),
    ('https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html/serverless-application-model-updates.rss', 'hhh6jr8858')
    ])
def test_hash_6(given, expected):
    encoder = CharSetEncoder(digest_size=6)
    assert encoder.hash(given) == expected


# _____________________________________________________________________________
@pytest.mark.parametrize('given, expected', [
    (1, 1),
])
def test_encode_decode(given, expected):
    encoder = CharSetEncoder()
    assert encoder.decode(encoder.encode(given)) == expected

from backend.models.sentences import get_sentences_by_ids
# need to fix
def test_get_sentences_by_ids():
    # Test 1
    sentence_ids = [61088, 61089]
    expected_output = {
        61088: {'sentence_id': 61088, 'chinese': '我们试试看！', 'pinyin': 'wǒ men shì shì kàn ！', 'english': "Let's try it."},
        61089: {'sentence_id': 61089, 'chinese': '我该去睡觉了。', 'pinyin': 'wǒ gāi qù shuì jiào le 。', 'english': 'I have to go to sleep.'}
    }
    assert get_sentences_by_ids(sentence_ids) == expected_output

    # Test 2
    sentence_ids = [61090]
    expected_output = {
        61090: {'sentence_id': 61090, 'chinese': '你在干什么啊？', 'pinyin': 'nǐ zài gàn shén me a ？', 'english': "What are you doing?"}
    }
    assert get_sentences_by_ids(sentence_ids) == expected_output
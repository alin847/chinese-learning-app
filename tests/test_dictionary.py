from backend.src.models.dictionary import get_search_results, get_word_by_id, get_word_ids_by_hsk


def test_get_search_results():
    # Test searching by simplified character
    results = get_search_results('simplified', '汉', limit=10)
    assert len(results) == 2, "Expected 2 results for '汉'"
    assert results[0]['simplified_id'] == 149592, "First result should have ID 149592"
    assert results[0]['simplified'] == '汉', "First result should be '汉'"
    assert results[0]['pinyin'] == 'hàn', "Pinyin for '汉' should be 'hàn'"
    assert results[0]['definitions'] == ['Han ethnic group', 
                                      'Chinese (language)', 
                                      'the Han dynasty (206 BC-220 AD)'], "Definitions for '汉' do not match"
    assert results[0]['sentence_ids'] == [61797, 61798, 61826], "Sentence IDs for '汉' do not match"
    assert results[1]['simplified_id'] == 149593, "Second result should have ID 149593"
    assert results[1]['simplified'] == '汉', "Second result should be '汉'"
    assert results[1]['pinyin'] == 'hàn', "Pinyin for '汉' should be 'hàn'"
    assert results[1]['definitions'] == ['man'], "Definitions for '汉' do not match"
    assert results[1]['sentence_ids'] == [61797, 61798, 61826], "Sentence IDs for '汉' do not match"
    
    # Test searching by pinyin
    results = get_search_results('pinyin_normalized', 'xinniankuaile', limit=10)
    assert len(results) == 10, "Expected 10 result for 'xinniankuaile'"
    assert results[0]['simplified_id'] == 133845, "First result should have ID 133845"
    assert results[0]['simplified'] == '新年快乐', "First result should be '新年快乐'"
    assert results[0]['pinyin'] == 'xīnniánkuàilè', "Pinyin for '新年快乐' should be 'xīnniánkuàilè'"
    assert results[0]['definitions'] == ['Happy New Year!'], "Definitions for '新年快乐' do not match"
    assert results[1]['simplified_id'] == 90772, "Second result should have ID 90772"
    assert results[1]['simplified'] == '信念', "Second result should be '信念'"
    assert results[1]['pinyin'] == 'xìnniàn', "Pinyin for '信念' should be 'xìnniàn'"
    assert results[1]['definitions'] == ["faith", "belief", "conviction"], "Definitions for '信念' do not match"

    # Test searching by definitions
    results = get_search_results('definitions', 'keyboard', limit=2)
    assert len(results) == 2, "Expected 2 result for 'keyboard'"
    assert results[0]['simplified_id'] == 193363, "First result should have ID 193363"
    assert results[0]['simplified'] == '键盘', "First result should be '键盘'"
    assert results[0]['pinyin'] == 'jiànpán', "Pinyin for '键盘' should be 'jiànpán'"
    assert results[0]['definitions'] == ['keyboard'], "Definitions for '键盘' do not match"
    assert results[1]['simplified_id'] == 193364, "Second result should have ID 193364"
    assert results[1]['simplified'] == '键盘侠', "Second result should be '键盘侠'"
    assert results[1]['pinyin'] == 'jiànpánxiá', "Pinyin for '键盘侠' should be 'jiànpánxiá'"
    assert results[1]['definitions'] == ['keyboard warrior'], "Definitions for '键盘侠' do not match"


def test_get_search_results_empty():
    # Test searching with a non-existent character
    results = get_search_results('simplified', '不存在', limit=10)
    assert len(results) == 0, "Expected no results for non-existent character"


def test_get_word_by_id():
    # Test retrieving a word by ID
    word = get_word_by_id(82020)
    assert isinstance(word, dict), "Expected a list of size 1 for ID"
    assert word['simplified_id'] == 82020, "Expected ID to be 82020"
    assert word['simplified'] == '一打', "Expected simplified character to be '一打'"
    assert word['pinyin'] == 'yīdǎ', "Expected pinyin to be 'yīdǎ'"
    assert word['definitions'] == ['dozen'], "Expected definitions to match"
    assert word['sentence_ids'] == [63741, 65722, 74633], "Expected sentence IDs to match"
    
    # Test retrieving a word with an invalid ID
    word = get_word_by_id(1)
    assert not word, "Expected no word object for invalid ID 1"

def test_get_word_by_id_batch():
    # Test retrieving multiple words by IDs
    ids = [82020, 149592, 149593]
    words = get_word_by_id(ids)
    assert len(words) == 3, "Expected 3 words for the given IDs"
    
    # Check the simplified characters
    assert words[0]['simplified'] == '一打', "First word should be '一打'"
    assert words[1]['simplified'] == '汉', "Second word should be '汉'"
    assert words[2]['simplified'] == '汉', "Third word should be '汉'"


def test_get_word_ids_by_hsk():
    # Test retrieving word IDs by HSK level
    hsk1_ids = get_word_ids_by_hsk(1)
    assert len(hsk1_ids) == 507, "Expected 507 words for HSK 1"
    
    hsk2_ids = get_word_ids_by_hsk(2)
    assert len(hsk2_ids) == 786, "Expected 786 words for HSK 2"
    
    hsk3_ids = get_word_ids_by_hsk(3)
    assert len(hsk3_ids) == 1004, "Expected 1004 words for HSK 3"
    
    # Test with an invalid HSK level
    hsk_invalid_ids = get_word_ids_by_hsk(10)
    assert len(hsk_invalid_ids) == 0, "Expected no words for invalid HSK level"
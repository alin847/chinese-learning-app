from app.models.dictionary import get_search_results, get_word_by_id

def test_get_search_results():
    # Test searching by simplified character
    results = get_search_results('simplified', '汉', limit=10)
    assert len(results) == 2, "Expected 2 results for '汉'"
    assert results[0]['id'] == 149592, "First result should have ID 149592"
    assert results[0]['simplified'] == '汉', "First result should be '汉'"
    assert results[0]['pinyin'] == 'hàn', "Pinyin for '汉' should be 'hàn'"
    assert results[0]['definitions'] == ['Han ethnic group', 
                                      'Chinese (language)', 
                                      'the Han dynasty (206 BC-220 AD)'], "Definitions for '汉' do not match"
    assert results[1]['id'] == 149593, "Second result should have ID 149593"
    assert results[1]['simplified'] == '汉', "Second result should be '汉'"
    assert results[1]['pinyin'] == 'hàn', "Pinyin for '汉' should be 'hàn'"
    assert results[1]['definitions'] == ['man'], "Definitions for '汉' do not match"

    # Test searching by pinyin
    results = get_search_results('pinyin_normalized', 'xinniankuaile', limit=10)
    assert len(results) == 10, "Expected 10 result for 'xinniankuaile'"
    assert results[0]['id'] == 133845, "First result should have ID 133845"
    assert results[0]['simplified'] == '新年快乐', "First result should be '新年快乐'"
    assert results[0]['pinyin'] == 'xīnniánkuàilè', "Pinyin for '新年快乐' should be 'xīnniánkuàilè'"
    assert results[0]['definitions'] == ['Happy New Year!'], "Definitions for '新年快乐' do not match"
    assert results[1]['id'] == 133843, "Second result should have ID 133846"
    assert results[1]['simplified'] == '新年', "Second result should be '新年'"
    assert results[1]['pinyin'] == 'xīnnián', "Pinyin for '新年' should be 'xīnnián'"
    assert results[1]['definitions'] == ['New Year', 'CL:個|个[ge4]'], "Definitions for '新年' do not match"

    # Test searching by definitions
    results = get_search_results('definitions', 'keyboard', limit=2)
    assert len(results) == 2, "Expected 2 result for 'keyboard'"
    assert results[0]['id'] == 193363, "First result should have ID 193363"
    assert results[0]['simplified'] == '键盘', "First result should be '键盘'"
    assert results[0]['pinyin'] == 'jiànpán', "Pinyin for '键盘' should be 'jiànpán'"
    assert results[0]['definitions'] == ['keyboard'], "Definitions for '键盘' do not match"
    assert results[1]['id'] == 193364, "Second result should have ID 193364"
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
    assert word is not None, "Expected a word object for ID 1"
    assert word['id'] == 82020, "Expected ID to be 82020"
    assert word['simplified'] == '一打', "Expected simplified character to be '一打'"
    assert word['pinyin'] == 'yīdǎ', "Expected pinyin to be 'yīdǎ'"
    assert word['definitions'] == ['dozen'], "Expected definitions to match"

    # Test retrieving a word with an invalid ID
    word = get_word_by_id(1)
    assert word is None, "Expected no word object for invalid ID 1"

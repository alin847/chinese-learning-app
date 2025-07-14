from app.models.sentences import get_sentences_by_character

def test_get_sentences_by_character():
    # Test retrieving sentences containing a specific character
    results = get_sentences_by_character('水果', limit=3)
    assert len(results) == 3, "Expected 2 results for character '水果'"
    assert results[0]["id"] == 1123, "First result should have ID 1123"
    assert results[1]["id"] == 1786, "Second result should have ID 1786"
    assert results[2]["id"] == 1942, "Third result should have ID 1942"

    assert results[0]["chinese"] == "这种水果形状像橙子，味道像菠萝。"
    assert results[0]["english"] == "This fruit is shaped like an orange and tastes like a pineapple."
    assert results[0]["pinyin"] == "zhèzhǒngshuǐguǒxíngzhuàngxiàngchéngzi，wèidàoxiàngbōluó。" 
    
    # Test retrieving sentences with a character that has no results
    results = get_sentences_by_character('八地是', limit=3)
    assert len(results) == 0, "Expected no results for character '八地是'"
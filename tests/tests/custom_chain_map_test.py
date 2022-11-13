from typing import Tuple

from game.game import CustomChainMap


def get_chain_map() -> Tuple[dict, dict, dict, CustomChainMap]:
    dic1 = {1: 1, 2: 2, 3: 3}
    dic2 = {4: 4, 5: 5, 6: 6}
    dic3 = {7: 7, 8: 8, 9: 9}
    chain = CustomChainMap([dic1, dic2, dic3])
    return dic1, dic2, dic3, chain


def test_getting_element() -> None:
    dic1, dic2, dic3, chain = get_chain_map()
    original_values = {}
    chain_values = {}
    for key, value in (dic1 | dic2 | dic3).items():
        original_values[key] = value
        chain_values[key] = chain[key]
    assert original_values == chain_values


def test_removing_element_from_source() -> None:
    dic1, dic2, dic3, chain = get_chain_map()
    del dic1[1]
    del dic2[5]
    del dic3[9]
    original_values = {}
    chain_values = {}
    for key, value in (dic1 | dic2 | dic3).items():
        original_values[key] = value
        chain_values[key] = chain[key]
    assert original_values == chain_values


def test_removing_element_from_chain() -> None:
    dic1, dic2, dic3, chain = get_chain_map()
    chain.remove(1)
    chain.remove(5)
    chain.remove(9)
    original_values = {}
    chain_values = {}
    for key, value in (dic1 | dic2 | dic3).items():
        original_values[key] = value
        chain_values[key] = chain[key]
    assert original_values == chain_values

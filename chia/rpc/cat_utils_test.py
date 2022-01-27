
from typing import Any, Dict
from chia.rpc.cat_utils import convert_to_parent_coin_spends, convert_to_cat_coins
from chia.types.coin_spend import CoinSpend
from chia.util.byte_types import hexstr_to_bytes
from chia.types.blockchain_format.sized_bytes import bytes32
from blspy import PrivateKey


def get_sample_raw_cat_coin(amount: int) -> Dict[str, Any]:
    return {
        "amount": amount,
        "parent_coin_info": "0x8599cc835a767775c655025fcd4249170d37affc4f4a85c830d8a41a93c1ea37",
        "puzzle_hash": "0x92a0803576cf48723aa77cfb5ec0e8b7f3e479799a81741aab50a621176d374b"
    }


def test_convert_to_cat_coins() -> None:
    asset_id_hex = "3d3615bb3848dada4093476ff1b9dbec633b7e2fd754766b4a1b23a858557590"
    sender_private_key_hex = "0x173e5da7060cad891ad2531f793fe0856a4841c6aafe9bb5ba177ba7bfddeeb3"

    asset_id: bytes32 = hexstr_to_bytes(asset_id_hex)
    sender_private_key_bytes: bytes32 = hexstr_to_bytes(sender_private_key_hex)
    sender_private_key: PrivateKey = PrivateKey.from_bytes(sender_private_key_bytes)

    res: Dict[str, CoinSpend] = convert_to_cat_coins(
        target_asset_id=asset_id,
        sender_private_key=sender_private_key,
        raw_cat_coins_pool=[
            get_sample_raw_cat_coin(amount=100),
            get_sample_raw_cat_coin(amount=200),
        ],
    )
    assert res != None
    assert len(res) == 2

    res: Dict[str, CoinSpend] = convert_to_cat_coins(
        target_asset_id=asset_id,
        sender_private_key=sender_private_key,
        raw_cat_coins_pool=[
            get_sample_raw_cat_coin(amount=100),
            get_sample_raw_cat_coin(amount=100),
        ],
    )
    assert res != None
    assert len(res) == 1


def get_default_raw_coin_spend() -> Dict[str, Any]:
    return {
        "coin": {
            "amount": 24330,
            "parent_coin_info": "0x8599cc835a767775c655025fcd4249170d37affc4f4a85c830d8a41a93c1ea37",
            "puzzle_hash": "0xa0557e2022d2d4803ad6b3638a909118d18ad8ccbecc844557b34f268f78938a"
        },
        "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ff5effff04ff02ffff04ffff04ff05ffff04ffff0bff2cff0580ffff04ff0bff80808080ffff04ffff02ff17ff2f80ffff04ff5fffff04ffff02ff2effff04ff02ffff04ff17ff80808080ffff04ffff0bff82027fff82057fff820b7f80ffff04ff81bfffff04ff82017fffff04ff8202ffffff04ff8205ffffff04ff820bffff80808080808080808080808080ffff04ffff01ffffffff81ca3dff46ff0233ffff3c04ff01ff0181cbffffff02ff02ffff03ff05ffff01ff02ff32ffff04ff02ffff04ff0dffff04ffff0bff22ffff0bff2cff3480ffff0bff22ffff0bff22ffff0bff2cff5c80ff0980ffff0bff22ff0bffff0bff2cff8080808080ff8080808080ffff010b80ff0180ffff02ffff03ff0bffff01ff02ffff03ffff09ffff02ff2effff04ff02ffff04ff13ff80808080ff820b9f80ffff01ff02ff26ffff04ff02ffff04ffff02ff13ffff04ff5fffff04ff17ffff04ff2fffff04ff81bfffff04ff82017fffff04ff1bff8080808080808080ffff04ff82017fff8080808080ffff01ff088080ff0180ffff01ff02ffff03ff17ffff01ff02ffff03ffff20ff81bf80ffff0182017fffff01ff088080ff0180ffff01ff088080ff018080ff0180ffff04ffff04ff05ff2780ffff04ffff10ff0bff5780ff778080ff02ffff03ff05ffff01ff02ffff03ffff09ffff02ffff03ffff09ff11ff7880ffff0159ff8080ff0180ffff01818f80ffff01ff02ff7affff04ff02ffff04ff0dffff04ff0bffff04ffff04ff81b9ff82017980ff808080808080ffff01ff02ff5affff04ff02ffff04ffff02ffff03ffff09ff11ff7880ffff01ff04ff78ffff04ffff02ff36ffff04ff02ffff04ff13ffff04ff29ffff04ffff0bff2cff5b80ffff04ff2bff80808080808080ff398080ffff01ff02ffff03ffff09ff11ff2480ffff01ff04ff24ffff04ffff0bff20ff2980ff398080ffff010980ff018080ff0180ffff04ffff02ffff03ffff09ff11ff7880ffff0159ff8080ff0180ffff04ffff02ff7affff04ff02ffff04ff0dffff04ff0bffff04ff17ff808080808080ff80808080808080ff0180ffff01ff04ff80ffff04ff80ff17808080ff0180ffffff02ffff03ff05ffff01ff04ff09ffff02ff26ffff04ff02ffff04ff0dffff04ff0bff808080808080ffff010b80ff0180ff0bff22ffff0bff2cff5880ffff0bff22ffff0bff22ffff0bff2cff5c80ff0580ffff0bff22ffff02ff32ffff04ff02ffff04ff07ffff04ffff0bff2cff2c80ff8080808080ffff0bff2cff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff2effff04ff02ffff04ff09ff80808080ffff02ff2effff04ff02ffff04ff0dff8080808080ffff01ff0bff2cff058080ff0180ffff04ffff04ff28ffff04ff5fff808080ffff02ff7effff04ff02ffff04ffff04ffff04ff2fff0580ffff04ff5fff82017f8080ffff04ffff02ff7affff04ff02ffff04ff0bffff04ff05ffff01ff808080808080ffff04ff17ffff04ff81bfffff04ff82017fffff04ffff0bff8204ffffff02ff36ffff04ff02ffff04ff09ffff04ff820affffff04ffff0bff2cff2d80ffff04ff15ff80808080808080ff8216ff80ffff04ff8205ffffff04ff820bffff808080808080808080808080ff02ff2affff04ff02ffff04ff5fffff04ff3bffff04ffff02ffff03ff17ffff01ff09ff2dffff0bff27ffff02ff36ffff04ff02ffff04ff29ffff04ff57ffff04ffff0bff2cff81b980ffff04ff59ff80808080808080ff81b78080ff8080ff0180ffff04ff17ffff04ff05ffff04ff8202ffffff04ffff04ffff04ff24ffff04ffff0bff7cff2fff82017f80ff808080ffff04ffff04ff30ffff04ffff0bff81bfffff0bff7cff15ffff10ff82017fffff11ff8202dfff2b80ff8202ff808080ff808080ff138080ff80808080808080808080ff018080ffff04ffff01a072dec062874cd4d3aab892a0906688a1ae412b0109982e1797a170add88bdcdcffff04ffff01a06d95dae356e32a71db5ddcb42224754a02524c615c5fc35f568c2af04774e589ffff04ffff01ff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b0aa6ba386d20dacfcb80023ca04d6978861fb9cee414d6a3db65cf0d37293f689560a59e2600f77f600118e6280ded67bff018080ff0180808080",
        "solution": "0xffff80ffff01ffff33ffa0104a5305c79a3ab77e82de41e5f42742a15d247e5262d80543dcf8da6593b4efff823a98ffffa0104a5305c79a3ab77e82de41e5f42742a15d247e5262d80543dcf8da6593b4ef8080ffff33ffa001d9ddec88f6603ef68ab75a3c024c5fd064c8b9b5ed8511a5e6cf0ec4dbb700ff8248b28080ff8080ffffa0fa0fb9a5922ffd72ef6ff3bbb1348fd5b3fb2496dc7964753a043adceeef46cbffa0bae24162efbd568f89bc7a340798a6118df0189eb9e3f8697bcea27af99f8f79ff825f0a80ffa0f20bf9087afdfb326852bcfd666215c55978f4b6dbbb74623df5f61b4531ae08ffffa08599cc835a767775c655025fcd4249170d37affc4f4a85c830d8a41a93c1ea37ffa0a0557e2022d2d4803ad6b3638a909118d18ad8ccbecc844557b34f268f78938aff825f0a80ffffa07787d6c07ef52bef3f9a3abced51a2f0f93bcc1d143a18b6b9db99d1eed9dcb6ffa08879350220c63a45da7bf8a158631cc88136c03541dad2f2d7e2872b621488ccff8203a280ff822440ff8080"
    }


def test_convert_to_parent_coin_spends() -> None:
    res: Dict[str, CoinSpend] = convert_to_parent_coin_spends(
        raw_parent_coin_spends={
            "abc": get_default_raw_coin_spend(),
            "xyz": get_default_raw_coin_spend(),
        },
    )
    assert res != None
    assert len(res) == 2


test_convert_to_cat_coins()
test_convert_to_parent_coin_spends()

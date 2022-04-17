from scripts.logic.PriceLogic import PriceLogic
from scripts.logic.helpers import absolute_error


# def test_get_parameters_returns_proper_values():
#     l = 20_000
#     h = 100_000
#     n = 2_000
#     m = 100
#     d = (h - l) / n
#     (a, c) = get_parameters(l, h, n, m)
#     expected_a = 0.00342243
#     expected_c = -9.38401

#     assert absolute_error(a, expected_a) < 0.1, f"{a=} {expected_a=}"
#     assert absolute_error(c, expected_c) < 0.1, f"{a=} {expected_a=}"


def test_get_parameters_returns_good_parameters():
    l = 20_000
    h = 100_000
    n = 2_000

    for m in range(10, 100_000, 2):
        price_logic = PriceLogic(l, h, n, m)

        assert (
                absolute_error(price_logic.get_usd_to_exchange(l, "buy"), 0.8 * m)
                < 0.000001
        )
        assert (
                absolute_error(price_logic.get_usd_to_exchange(h, "buy"), 0.01 * m)
                < 0.000001
        )

        assert (
                absolute_error(price_logic.get_usd_to_exchange(h, "sell"), 0.8 * m)
                < 0.000001
        )
        assert (
                absolute_error(price_logic.get_usd_to_exchange(l, "sell"), 0.01 * m)
                < 0.000001
        )

# def test_get_usd_to_exchange_returns_proper_values():
#     l = 20_000
#     h = 100_000
#     n = 2_000
#     m = 100
#     d = (h - l) / n
#     (a, b) = get_parameters(l, h, n, m)
#     # # a = 0.00342243
#     # c = -9.38401
#     assert floor(get_usd_to_exchange(h, a, c)) == 0.66 * m, f"{a=} {c=}"

#     all = 0
#     for i in range(n + 1):
#         print(get_usd_to_spend(l + i * d, a, c))
#         all += get_usd_to_spend(l + i * d, a, c)
#     assert floor(all) == m, f"{a=} {c=}"

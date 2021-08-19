from python_task.main import get_data


def test_no_filter():
    # This test will fail once the data updates remotely,
    # but it's the easiest way to check right now that all data is fetched
    assert len(list(get_data(10, lambda x: True))) == 157


def test_filter():
    all_items = list(get_data(10, lambda x: True))
    filtered_items = list(get_data(10, lambda x: x['commission']['max']['unit'] == '%'))
    assert all([x['commission']['max']['unit'] == '%' for x in filtered_items])

    contains_percent = [x for x in all_items if x['commission']['max']['unit'] == '%']
    assert contains_percent == filtered_items
    not_in_filtered = [x for x in all_items if x not in filtered_items]
    assert all([x['commission']['max']['unit'] != '%' for x in not_in_filtered])

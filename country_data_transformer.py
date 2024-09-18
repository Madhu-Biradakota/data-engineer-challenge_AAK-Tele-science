from bs4 import BeautifulSoup


# Function to transform the overview data
def parse_overview_data(overview_panel_html):
    print("parse_overview_data in function ")
    overview_data = []
    soup = BeautifulSoup(overview_panel_html, 'html.parser')

    # Find all indicator topics (e.g., Social, Economic, etc.)
    topics = soup.find_all('div', class_='indicator-item')

    for topic in topics:
        indicator_data = {}

        # Extract the topic title (e.g., Social, Economic)
        title = topic.find('h1')
        if title:
            indicator_data['Topic'] = title.text.strip()

        # List to store indicators within each topic
        indicator_data['Indicators'] = []

        # Extract individual indicators under each topic
        indicator_items = topic.find_all('div', class_='indicator-item__wrapper')
        for item in indicator_items:
            item_data = {}

            # Extract the individual indicator title
            indicator_title = item.find('div', class_='indicator-item__title')
            if indicator_title:
                item_data['Indicator'] = indicator_title.text.strip()

            # Extract the most recent value
            recent_value_section = item.find('div', class_='indicator-item__col--middle')
            if recent_value_section:
                no_data = recent_value_section.find('p', class_='indicator-item__data-info-empty')
                if no_data:
                    item_data['Most recent value'] = no_data.find('span').text.strip()
                else:
                    data_value = recent_value_section.find('div', class_='indicator-item__data-info')
                    if data_value:
                        value_span = data_value.find('span')
                        if value_span:
                            item_data['Most recent value'] = value_span.text.strip()

                        # Extract the year for the data (if available)
                        year_info = recent_value_section.find('p', class_='indicator-item__data-info-year')
                        if year_info:
                            item_data['Year'] = year_info.text.strip()

            # Add the trend data if available
            trend_section = item.find('div', class_='indicator-item__col--last')
            if trend_section:
                chart_wrap = trend_section.find('div', class_='indicator-item__chart-inner-wrap')
                if chart_wrap:
                    item_data['Trend'] = chart_function(chart_wrap)

            # Append the indicator data to the topic
            indicator_data['Indicators'].append(item_data)

        # Append the topic data to overview
        overview_data.append(indicator_data)

    print(overview_data)
    return overview_data


# Function to transform the theme data (from 'By Theme' tab)
def parse_theme_data(theme_panel_html):
    theme_data = []

    soup = BeautifulSoup(theme_panel_html, 'html.parser')
    topics = soup.find_all('div', class_='indicator-item')

    for topic in topics:
        indicator_data = {}

        # Extract the title of the topic
        title = topic.find('h1')
        if title:
            indicator_data['Theme'] = title.text.strip()

        indicator_data['Indicators'] = []

        # Extract individual indicators within each section
        indicator_items = topic.find_all('div', class_='indicator-item__wrapper')
        for item in indicator_items:
            item_data = {}

            # Extract the individual indicator title
            indicator_title = item.find('div', class_='indicator-item__title')
            if indicator_title:
                item_data['Indicator'] = indicator_title.text.strip()

            # Extract the most recent value
            recent_value_section = item.find('div', class_='indicator-item__col--middle')
            if recent_value_section:
                no_data = recent_value_section.find('p', class_='indicator-item__data-info-empty')
                if no_data:
                    item_data['Most recent value'] = no_data.find('span').text.strip()
                else:
                    data_value = recent_value_section.find('div', class_='indicator-item__data-info')
                    if data_value:
                        value_span = data_value.find('span')
                        if value_span:
                            item_data['Most recent value'] = value_span.text.strip()

                        year_info = recent_value_section.find('p', class_='indicator-item__data-info-year')
                        if year_info:
                            item_data['Year'] = year_info.text.strip()

            # Extract the trend HTML content from 'item'
            trend_section = item.find('div', class_='indicator-item__col--last')
            if trend_section:
                chart_wrap = trend_section.find('div', class_='indicator-item__chart-inner-wrap')
                if chart_wrap:
                    item_data['Trend'] = chart_function(chart_wrap)

            indicator_data['Indicators'].append(item_data)

        theme_data.append(indicator_data)

    print(theme_data)
    return theme_data


# Function to transform the SDG data (from 'By SDG Goal' tab)
def parse_sdg_data(sdg_panel_html):
    sdg_data = []

    soup = BeautifulSoup(sdg_panel_html, 'html.parser')
    topics = soup.find_all('div', class_='indicator-item')

    for topic in topics:
        indicator_data = {}

        # Extract the SDG goal title
        title = topic.find('h1')
        if title:
            indicator_data['SDG Goal'] = title.text.strip()

        indicator_data['Indicators'] = []

        # Extract individual indicators within each SDG goal section
        indicator_items = topic.find_all('div', class_='indicator-item__wrapper')
        for item in indicator_items:
            item_data = {}

            # Extract the individual indicator title
            indicator_title = item.find('div', class_='indicator-item__title')
            if indicator_title:
                item_data['Indicator'] = indicator_title.text.strip()

            # Extract the most recent value
            recent_value_section = item.find('div', class_='indicator-item__col--middle')
            if recent_value_section:
                no_data = recent_value_section.find('p', class_='indicator-item__data-info-empty')
                if no_data:
                    item_data['Most recent value'] = no_data.find('span').text.strip()
                else:
                    data_value = recent_value_section.find('div', class_='indicator-item__data-info')
                    if data_value:
                        value_span = data_value.find('span')
                        if value_span:
                            item_data['Most recent value'] = value_span.text.strip()

                        year_info = recent_value_section.find('p', class_='indicator-item__data-info-year')
                        if year_info:
                            item_data['Year'] = year_info.text.strip()

            # Extract the trend HTML content from 'item'
            trend_section = item.find('div', class_='indicator-item__col--last')
            if trend_section:
                chart_wrap = trend_section.find('div', class_='indicator-item__chart-inner-wrap')
                if chart_wrap:
                    item_data['Trend'] = chart_function(chart_wrap)

            indicator_data['Indicators'].append(item_data)

        sdg_data.append(indicator_data)

    print(sdg_data)
    return sdg_data


# Function to extract the chart data (Trend)
def chart_function(chart_data):
    # Check for 'no-data' div
    no_data_div = chart_data.find('div', class_='no-data')
    if no_data_div and no_data_div.get('style') == 'display: block;':
        no_data_message = no_data_div.find('h2').text.strip() if no_data_div.find('h2') else 'No trend data available'
        return no_data_message

    # Otherwise, extract the SVG content representing the trend
    svg_element = chart_data.find('svg')
    if svg_element:
        return "The trend is available(svg element)"

    return "No trend data available"

# Example usage (assuming you already have the extracted HTML for each section)
# overview_html, theme_html, sdg_html = <HTML content>
# parse_overview_data(overview_html)
# parse_theme_data(theme_html)
# parse_sdg_data(sdg_html)
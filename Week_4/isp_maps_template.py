"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """

    with open(codeinfo['codefile'], newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=codeinfo['separator'],
                                quotechar=codeinfo['quote'])
        table = {row[codeinfo['plot_codes']]: row[codeinfo['data_codes']] for row in reader}
    return table


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """

    table = build_country_code_converter(codeinfo)
    matching = {}
    not_matching = set()
    lower_table = {i.lower(): table[i].lower() for i in table}
    lower_data = {i.lower(): i for i in gdp_countries}
    for key in plot_countries:
        if key.lower() not in lower_table:
            not_matching.add(key)
            continue
        data_key = lower_table[key.lower()]
        if data_key in lower_data:
            matching[key] = lower_data[data_key]
        else:
            not_matching.add(key)
    return matching, not_matching


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """

    avaliable = {}
    not_avaliable = set()
    with open(gdpinfo["gdpfile"], newline='') as csvfile:
        gdp_countries = {}
        for row in csv.DictReader(csvfile,
                                  delimiter=gdpinfo["separator"],
                                  quotechar=gdpinfo["quote"]):
            rowid = row[gdpinfo["country_code"]]
            gdp_countries[rowid] = dict(row)

    matching, not_matching = reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
    not_matching = {i.upper() for i in not_matching}
    for key in matching:
        data_code = matching[key]
        temp_data = gdp_countries[data_code][year]
        if temp_data != '':
            avaliable[key.upper()] = math.log10(float(temp_data))
        else:
            not_avaliable.add(key.upper())
    return avaliable, not_matching, not_avaliable


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """

    avaliable, not_matching, not_avaliable = build_map_dict_by_code(gdpinfo,
                                                                    codeinfo,
                                                                    plot_countries,
                                                                    year)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.add("GDP for "+year, avaliable)
    worldmap_chart.add("Missing from World Bank Data", not_matching)
    worldmap_chart.add("No GDP data", not_avaliable)
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "./Datasets/isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "./Datasets/isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
# test_build_map_dict_by_code()

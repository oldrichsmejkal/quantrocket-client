# Copyright 2017 QuantRocket - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

def add_subparser(subparsers):
    _parser = subparsers.add_parser("master", description="QuantRocket securities master CLI", help="quantrocket master -h")
    _subparsers = _parser.add_subparsers(title="subcommands", dest="subcommand")
    _subparsers.required = True


    examples = """
Examples:
List all exchanges:

    quantrocket master exchanges

List stock exchanges in North America:

    quantrocket master exchanges --regions north_america --sec-types STK
    """
    parser = _subparsers.add_parser(
        "exchanges", help="list exchanges by security type and country as found on the IB website", epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-r", "--regions", nargs="*", choices=["north_america", "europe", "asia", "global"],
        metavar="REGION", help="limit to these regions")
    parser.add_argument(
        "-s", "--sec-types", nargs="*",
        choices=["STK", "ETF", "FUT", "CASH", "IND"], metavar="SEC_TYPE", help="limit to these security types")
    parser.set_defaults(func="quantrocket.master._cli_list_exchanges")

    examples = """
Specify an exchange (optionally filtering by security type, currency, and/or symbol) to fetch
listings from the IB website and pull associated contract details from the IB API. Or, specify groups
or conids to pull details from the IB API, bypassing the website.

Examples:
Pull all Toronto Stock Exchange stocks listings:

    quantrocket master listings --exchange TSE --sec-types STK

Pull all NYSE ARCA ETF listings:

    quantrocket master listings --exchange ARCA --sec-types ETF

Pull specific symbols from Nasdaq (ISLAND):

    quantrocket master listings --exchange ISLAND --symbols AAPL GOOG NFLX

Re-pull contract details for an existing securities group called "japan-fin":

    quantrocket master listings --groups "japan-fin"
    """
    parser = _subparsers.add_parser(
        "listings", help="pull securities listings from IB into securities master database, either by exchange or by groups/conids", epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-e", "--exchange", metavar="EXCHANGE", help="the exchange code to pull listings for (required unless providing groups or conids)")
    parser.add_argument(
        "-t", "--sec-types", nargs="*", metavar="SEC_TYPE",
        choices=["STK", "ETF", "FUT", "CASH", "IND"], help="limit to these security types")
    parser.add_argument("-c", "--currencies", nargs="*", metavar="CURRENCY", help="limit to these currencies")
    parser.add_argument("-s", "--symbols", nargs="*", metavar="SYMBOL", help="limit to these symbols")
    parser.add_argument("-g", "--groups", nargs="*", metavar="GROUP", help="limit to these groups")
    parser.add_argument("-i", "--conids", nargs="*", metavar="CONID", help="limit to these conids")
    parser.set_defaults(func="quantrocket.master._cli_pull_listings")

    query_parent_parser = argparse.ArgumentParser(add_help=False)
    filters = query_parent_parser.add_argument_group("filtering options")
    filters.add_argument("-e", "--exchanges", nargs="*", metavar="EXCHANGE", help="limit to these exchanges")
    filters.add_argument("-t", "--sec-types", nargs="*", metavar="SEC_TYPE", choices=["STK", "ETF", "FUT", "CASH", "IND"], help="limit to these security types")
    filters.add_argument("-c", "--currencies", nargs="*", metavar="CURRENCY", help="limit to these currencies")
    filters.add_argument("-g", "--groups", nargs="*", metavar="GROUP", help="limit to these groups")
    filters.add_argument("-s", "--symbols", nargs="*", metavar="SYMBOL", help="limit to these symbols")
    filters.add_argument("-i", "--conids", nargs="*", metavar="CONID", help="limit to these conids")
    filters.add_argument("--exclude-groups", nargs="*", metavar="GROUP", help="exclude these groups")
    filters.add_argument("--exclude-conids", nargs="*", metavar="CONID", help="exclude these conids")
    filters.add_argument("--sectors", nargs="*", metavar="SECTOR", help="limit to these sectors")
    filters.add_argument("--industries", nargs="*", metavar="INDUSTRY", help="limit to these industries")
    filters.add_argument("--categories", nargs="*", metavar="CATEGORY", help="limit to these categories")
    filters.add_argument("-d", "--delisted", action="store_true", default=False, help="include delisted securities")

    examples = """
Examples:
Download a CSV of all securities in a group called "mexi-fut":

    quantrocket master get mexi.csv --groups "mexi-fut"

Download a CSV of all ARCA ETFs:

    quantrocket master get arca.csv --exchanges ARCA --sec-types ETF

    """
    parser = _subparsers.add_parser(
        "get", help="query security details from the securities master database and download to file", epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter, parents=[query_parent_parser])
    parser.add_argument("filepath_or_buffer", metavar="FILENAME", help="filename to write the data to")
    formats = parser.add_argument_group("formatting options")
    formats.add_argument("-j", "--json", action="store_const", const="json", dest="output", help="format output as JSON (default is CSV)")
    parser.set_defaults(func="quantrocket.master.download_securities_file")

    examples = """
Examples:
Get conids of all ARCA ETFs:

    quantrocket master conids --exchanges ARCA --sec-types ETF

Get conids of all consumer cyclicals trading on the Australian Stock Exchange:

    quantrocket master conids --exchanges ASX --sectors "Consumer, Cyclical"
    """
    parser = _subparsers.add_parser(
        "conids", help="query conids from the securities master database", epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter, parents=[query_parent_parser])
    parser.set_defaults(func="quantrocket.master._cli_get_conids")

    examples = """
Examples:
Get a diff for all securities in a group called "italy-stk":

    quantrocket master diff --groups "italy-stk"

Get a diff for all securities in a group called "italy-stk", looking only for sector or
industry changes:

    quantrocket master diff --groups "italy-stk" --fields Sector Industry

Get a diff for specific securities by conid:

    quantrocket master diff --conids 123456 234567

Get a diff for all securities in a group called "italy-stk" and log the results, if any,
to flightlog:

    quantrocket master diff --groups "italy-stk" | quantrocket flightlog log --loglevel WARNING --name "quantrocket.master"

Get a diff for all securities in a group called "nasdaq-sml" and auto-delist any symbols that
are no longer available from IB or that are now associated with the PINK exchange:

    quantrocket master diff --groups "nasdaq-sml" --delist-missing --delist-exchanges PINK
    """
    parser = _subparsers.add_parser(
        "diff", help="flag security details that have changed in IB's system since the time "
        "they were last loaded into the securities master database", epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-g", "--groups", nargs="*", metavar="GROUP", help="limit to these groups")
    parser.add_argument("-i", "--conids", nargs="*", metavar="CONID", help="limit to these conids")
    parser.add_argument("-f", "--fields", nargs="*", metavar="FIELD", help="only diff these fields")
    parser.add_argument("--delist-missing", action="store_true", default=False, help="auto-delist securities that are no longer available from IB")
    parser.add_argument("--delist-exchanges", metavar="EXCHANGE", nargs="*", help="auto-delist securities that are associated with these exchanges")
    parser.set_defaults(func="quantrocket.master._cli_diff_securities")

    parser = _subparsers.add_parser("group", help="create a group of securities meeting certain criteria")
    parser.add_argument("name", metavar="GROUP_NAME", help="the name to assign to the group")
    parser.add_argument("-e", "--exchange", metavar="EXCHANGE", help="limit to this exchange")
    parser.add_argument("-t", "--sec-type", dest="sec_type", choices=["STK", "FUT", "CASH"], help="limit to this security type")
    parser.add_argument("-c", "--currency", metavar="CURRENCY", help="limit to this currency")
    parser.add_argument("-n", "--min-liq", metavar="DOLLAR_VOLUME", type=int, help="limit to symbols where 90-day price X volume is greater than or equal to this number")
    parser.add_argument("-x", "--max-liq", metavar="DOLLAR_VOLUME", type=int, help="limit to symbols where 90-day price X volume is less than or equal to this number")
    parser.add_argument("--from-groups", nargs="*", metavar="GROUP", help="limit to symbols from these existing groups")
    parser.add_argument("-s", "--symbols", nargs="*", metavar="SYMBOL", help="limit to these symbols")
    parser.add_argument("-i", "--conids", nargs="*", metavar="CONID", help="limit to these conids")
    parser.add_argument("--sectors", nargs="*", metavar="SECTOR", help="limit to these sectors")
    parser.add_argument("--industries", nargs="*", metavar="INDUSTRY", help="limit to these industries")
    parser.add_argument("--categories", nargs="*", metavar="CATEGORY", help="limit to these categories")
    parser.add_argument("--exclude-delisted", action="store_true", dest="exclude_delisted", help="exclude delisted securities (default is to include them if they meet the criteria)")
    parser.add_argument("-f", "--input-file", metavar="FILENAME", help="create the group from the con_ids in this file")
    parser.add_argument("-a", "--append", action="store_true", help="append to group if group already exists")
    parser.set_defaults(func="quantrocket.master.create_group")

    parser = _subparsers.add_parser("rmgroup", help="remove a security group")
    parser.add_argument("group", help="the group name")
    parser.set_defaults(func="quantrocket.master.delete_group")

    parser = _subparsers.add_parser("frontmonth", help="return the frontmonth contract for a futures underlying, as of now or over a date range")
    parser.add_argument("symbol", help="the underlying's symbol (e.g. ES)")
    parser.add_argument("exchange", help="the exchange where the contract trades (e.g. GLOBEX)")
    parser.add_argument("-c", "--currency", metavar="CURRENCY", help="the contract's currency, if necessary to disambiguate")
    parser.add_argument("-m", "--multiplier", metavar="MULTIPLIER", help="the contract's multiplier, if necessary to disambiguate")
    parser.add_argument("-s", "--start-date", metavar="YYYY-MM-DD", help="return the frontmonth conid for each date on or after this date")
    parser.add_argument("-e", "--end-date", metavar="YYYY-MM-DD", help="return the frontmonth conid for each date on or before this date")
    parser.set_defaults(func="quantrocket.master.get_frontmonth")

    examples = """
Examples:
Upload a new rollover config (replaces current config):

    quantrocket master rollrules myrolloverrules.yml

Show current rollover config:

    quantrocket master rollrules
    """
    parser = _subparsers.add_parser(
        "rollrules", help="upload a new rollover rules config, or return the current rollover rules", epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("filename", nargs="?", metavar="FILENAME", help="the rollover rules config file to upload (if omitted, return the current config)")
    parser.set_defaults(func="quantrocket.master._cli_load_or_show_rollrules")

    parser = _subparsers.add_parser("delist", help="delist a security by con_id or symbol+exchange")
    parser.add_argument("-c", "--conid", type=int, help="the conid of the security to delist")
    parser.add_argument("-s", "--symbol", help="the symbol to be delisted")
    parser.add_argument("-e", "--exchange", help="the exchange of the symbol to be delisted")
    parser.set_defaults(func="quantrocket.master.delist")

    parser = _subparsers.add_parser("lots", help="load lot sizes from a file")
    parser.add_argument("filename", metavar="FILE", help="CSV file with columns 'lot_size' and either 'conid' or 'symbol' (and optionally 'exchange' and/or 'currency' for disambiguation)")
    parser.add_argument("-g", "--groups", metavar="GROUP", help="only try to match to securities in these groups (to prevent false matches in case of symbol ambiguity)")
    parser.set_defaults(func="quantrocket.master.load_lots")

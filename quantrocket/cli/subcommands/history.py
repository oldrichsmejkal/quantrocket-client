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

def add_subparser(subparsers):
    _parser = subparsers.add_parser("history", description="QuantRocket historical market data CLI", help="quantrocket history -h")
    _subparsers = _parser.add_subparsers(title="subcommands", dest="subcommand")
    _subparsers.required = True

    parser = _subparsers.add_parser("download", help="download historical market data for the named database(s)")
    parser.add_argument("databases", metavar="DB", nargs="+", help="the database key(s), for example 'canada'")
    parser.add_argument("-p", "--priority", action="store_true", help="use the priority queue (default is to use the standard queue)")
    parser.set_defaults(func="quantrocket.history.download")

    parser = _subparsers.add_parser("status", help="show info about pending and running downloads")
    parser.set_defaults(func="quantrocket.history.get_status")

    parser = _subparsers.add_parser("cancel", help="cancel a running or pending download")
    parser.add_argument("database", metavar="DB", help="the database key, for example 'canada'")
    parser.set_defaults(func="quantrocket.history.cancel_download")

    parser = _subparsers.add_parser("config", help="show the current configuration")
    parser.set_defaults(func="quantrocket.history.get_config")

    parser = _subparsers.add_parser("add", help="add a new config file to be merged with any existing config")
    parser.add_argument("config_file", metavar="CONFIG_FILE", help="the config file to add")
    parser.set_defaults(func="quantrocket.history.add_config")

    parser = _subparsers.add_parser("drop", help="delete a price history database and associated config")
    parser.add_argument("database", metavar="DB", help="the database key, for example 'canada'")
    parser.add_argument("--confirm-by-typing-db-name-again", dest="confirm_by_typing_db_name_again", required=True, help="enter the db name to confirm you want to drop it")
    parser.set_defaults(func="quantrocket.history.drop_database")
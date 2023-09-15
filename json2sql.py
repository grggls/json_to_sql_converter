import argparse
from json2sql import main as json_to_sql_main


def main():
    parser = argparse.ArgumentParser(description="Convert JSON to SQL")
    parser.add_argument("input_file", help="Path to the input JSON file")
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        json_data = f.read()

    # Call your library function to process the JSON data
    sql_query = json_to_sql_main(json_data)

    # Print or save the SQL query
    print(sql_query)


if __name__ == "__main__":
    main()

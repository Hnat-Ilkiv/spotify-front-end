import argparse
from src.command import generate_csv_command, import_csv_command


def main():
    parser = argparse.ArgumentParser(description="Spotify Data CLI")

    subparsers = parser.add_subparsers(dest='command', required=True)

    gen_csv_parser = subparsers.add_parser('gen_csv', help='Generation Spotify CSV')
    gen_csv_parser.add_argument('--path', type=str, default='data/spotify_data.csv', help='Path to CSV file')
    gen_csv_parser.add_argument('-s', action='store_true', help='Generate small CSV file')
    gen_csv_parser.add_argument('-m', action='store_true', help='Generate medium CSV file')
    gen_csv_parser.add_argument('-l', action='store_true', help='Generate large CSV file')
    gen_csv_parser.add_argument('--users', type=int, default=None, help='Number of Users generate')
    gen_csv_parser.add_argument('--playlists', type=int, default=None, help='Max number of Playlist for one User generate')
    gen_csv_parser.add_argument('--songs', type=int, default=None, help='Max number of Songs for one Playlist generate')
    gen_csv_parser.add_argument('--verbose', action='store_true', help='Enable verbose output mode')
    gen_csv_parser.set_defaults(func=generate_csv_command)

    import_csv_parser = subparsers.add_parser('import_csv', help='Import Spotify CSV to DB')
    import_csv_parser.add_argument('--path_csv', type=str, default='data/spotify_data.csv', help='Path to CSV file')
    import_csv_parser.add_argument('--path_db', type=str, default='data/spotify_data.db', help='Path to CSV file')
    import_csv_parser.add_argument('--verbose', action='store_true', help='Enable verbose output mode')
    import_csv_parser.set_defaults(func=import_csv_command)

    
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

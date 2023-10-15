def main():
    import argparse

    parser = argparse.ArgumentParser(description="Mehditor")
    parser.add_argument("filename", nargs="*", help="File to open")
    args = parser.parse_args()

    from mehditor.screens.mehditor_app import MeheditorApp

    if args.filename:
        app = MeheditorApp(file=args.filename[0])
        app.run()
    else:
        app = MeheditorApp(file=None)
        app.run()


if __name__ == "__main__":
    main()

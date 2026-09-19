"""Entry point for the local password generator/vault app."""

from ui.app import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

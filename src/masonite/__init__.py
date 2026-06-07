import warnings

__version__ = "4.20.4"

warnings.warn(
    "The 'masonite' package is unmaintained and will receive no further updates. "
    "Masonite 5 continues as 'masonite-framework' "
    "(https://github.com/masonitedev/masonite). Upgrade guide: "
    "https://docs.masonite.dev/upgrade-guide/masonite-4.0-to-5.0/",
    FutureWarning,
    stacklevel=2,
)

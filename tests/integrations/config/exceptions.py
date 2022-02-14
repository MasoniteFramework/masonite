OPTIONS = {
    "editor": "vscode",
    "search_url": "https://www.google.com/search?q=",
    "links": {
        "doc": "https://docs.masoniteproject.com",
        "repo": "https://github.com/MasoniteFramework/masonite",
    },
    "stack": {"offset": 10, "shorten": True},
    "hide_sensitive_data": True,
}

HANDLERS = {
    "dumps": True,
    "solutions": {"stackoverflow": False, "possible_solutions": True},
    "recommendations": {
        "packages_updates": {
            "list": ["exceptionite", "masonite", "masonite-orm", "pytest"]
        }
    },
}

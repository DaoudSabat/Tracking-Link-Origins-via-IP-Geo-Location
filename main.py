"""Entry point — CLI tool to trace a URL's origin server location."""
from core.link_tracer import LinkTracer


def main() -> None:
    tracer = LinkTracer()
    url = input("Enter a URL to trace: ").strip()
    result = tracer.trace(url)
    if result:
        print("\n--- Trace Result ---")
        for key, value in result.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("Could not trace the URL.")


if __name__ == "__main__":
    main()

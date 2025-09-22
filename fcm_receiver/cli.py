"""
Command line interface for FCM Receiver
"""

import argparse
import sys
from .core import FCMReceiver
from .exceptions import FCMReceiverError


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="FCM Receiver CLI"
    )
    parser.add_argument(
        "--credentials", "-c",
        required=True,
        help="Path to service account credentials JSON file"
    )
    parser.add_argument(
        "--project-id", "-p",
        required=True,
        help="Firebase project ID"
    )
    parser.add_argument(
        "--topic", "-t",
        help="Topic to subscribe to"
    )
    parser.add_argument(
        "--unsubscribe", "-u",
        action="store_true",
        help="Unsubscribe from topic instead of subscribing"
    )

    args = parser.parse_args()

    try:
        receiver = FCMReceiver(
            credentials_path=args.credentials,
            project_id=args.project_id
        )
        receiver.initialize()

        if args.topic:
            if args.unsubscribe:
                success = receiver.unsubscribe_from_topic(args.topic)
                if success:
                    print(f"Unsubscribed from topic: {args.topic}")
                else:
                    print(f"Failed to unsubscribe from topic: {args.topic}")
                    sys.exit(1)
            else:
                success = receiver.subscribe_to_topic(args.topic)
                if success:
                    print(f"Subscribed to topic: {args.topic}")
                else:
                    print(f"Failed to subscribe to topic: {args.topic}")
                    sys.exit(1)
        else:
            subscriptions = receiver.get_subscriptions()
            print("Current subscriptions:")
            for sub in subscriptions:
                print(f"  - {sub}")

    except FCMReceiverError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

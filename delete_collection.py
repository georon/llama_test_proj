import chromadb
import argparse
import asyncio

# Initialize the client
client = chromadb.HttpClient()  # or PersistentClient if you're using persistent storage

async def delete_collection(collection_name):
    """Delete a single collection by name"""
    try:
        client.delete_collection(name=collection_name)
        print(f"Successfully deleted collection: {collection_name}")
        return True
    except Exception as e:
        print(f"Error deleting collection {collection_name}: {str(e)}")
        return False

async def delete_all_collections():
    """Delete all collections in the database"""
    try:
        collections = client.list_collections()
        if not collections:
            print("No collections found to delete.")
            return
            
        print(f"Found {len(collections)} collections to delete...")
        for collection in collections:
            await delete_collection(collection.name)
        print("Finished deleting all collections.")
    except Exception as e:
        print(f"Error listing collections: {str(e)}")

# Set up argument parser
parser = argparse.ArgumentParser(description='Delete ChromaDB collection(s)')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('collection_name', nargs='?', help='Name of the collection to delete')
group.add_argument('--all', action='store_true', help='Delete all collections')
args = parser.parse_args()

# Initialize the client
client = chromadb.HttpClient()  # or PersistentClient if you're using persistent storage

if args.all:
    asyncio.run(delete_all_collections())
else:
    asyncio.run(delete_collection(args.collection_name))
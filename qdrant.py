from qdrant_client import QdrantClient
from qdrant_client.models import Filter

def main():
    client = QdrantClient(host='localhost', port=6333)
    collection_name = 'test_ylem'

    while True:
        print("\n=== Qdrant 관리 시스템 ===")
        print("1. 컬렉션 생성")
        print("2. 컬렉션 삭제")
        print("3. 컬렉션 검색")
        print("0. 종료")
        
        choice = input("\n원하는 작업의 번호를 입력하세요: ")
        
        if choice == "1":
            if not client.collection_exists(collection_name):
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config={"size": 1536, "distance": "Cosine"}
                )
                print(f"컬렉션 '{collection_name}'이 생성되었습니다.")
            else:
                print(f"컬렉션 '{collection_name}'이 이미 존재합니다.")
                
        elif choice == "2":
            if client.collection_exists(collection_name):
                client.delete_collection(collection_name)
                print(f"컬렉션 '{collection_name}'이 삭제되었습니다.")
            else:
                print(f"컬렉션 '{collection_name}'이 존재하지 않습니다.")
                
        elif choice == "3":
            if client.collection_exists(collection_name):
                response, _ = client.scroll(collection_name=collection_name)
                if response:
                    for point in response:
                        print(f"ID: {point.id}, Payload: {point.payload}")
                else:
                    print("컬렉션이 비어있습니다.")
            else:
                print(f"컬렉션 '{collection_name}'이 존재하지 않습니다.")
                
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
            
        else:
            print("잘못된 입력입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
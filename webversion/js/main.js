let fileDb, companyDb;
let fileDbInitialized = false;
let companyDbInitialized = false;

// IndexedDB 초기화 요청
const requestFileDb = indexedDB.open("FileDB", 1);
const requestCompanyDb = indexedDB.open("CompanyDB", 1);

// FileDB 설정 및 초기화
requestFileDb.onupgradeneeded = function(event) {
    fileDb = event.target.result;
    fileDb.createObjectStore("fileObjectStore", { keyPath: "id" });
};

requestFileDb.onsuccess = function(event) {
    fileDb = event.target.result;
    fileDbInitialized = true;
    checkInitialization();
};

requestFileDb.onerror = function(event) {
    console.error("Database error: " + event.target.errorCode);
};

// CompanyDB 설정 및 초기화
requestCompanyDb.onupgradeneeded = function(event) {
    companyDb = event.target.result;
    companyDb.createObjectStore("companyObjectStore", { keyPath: "id" });
};

requestCompanyDb.onsuccess = function(event) {
    companyDb = event.target.result;
    companyDbInitialized = true;
    checkInitialization();
};

requestCompanyDb.onerror = function(event) {
    console.error("Database error: " + event.target.errorCode);
};

function checkInitialization() {
    if (fileDbInitialized && companyDbInitialized) {
        initializeApp();
    }
}

function initializeApp() {
    $(document).ready(async function() {
        const urlParams = new URLSearchParams(window.location.search);
        let urlValue = urlParams.get('url');

        if (urlValue && urlValue.startsWith('http://')) {
            urlValue = urlValue.replace('http://', 'https://');
        }

        if (urlValue) {
            console.log("URL 파라미터 값:", urlValue);
        } else {
            console.log("'url' 파라미터가 존재하지 않습니다.");
        }

        $('#sync').on('click', async function () {
            let API_FILE_URL = urlValue + "/syncFiles";
            await fetchDataFromServer(API_FILE_URL, 'file');

            let API_COMP_URL = urlValue + "/syncCompanies";
            await fetchDataFromServer(API_COMP_URL, 'company');
        });

        $('#remove').on('click', async function () {
            try {
                await deleteAllData(fileDb, "fileObjectStore");
                await deleteAllData(companyDb, "companyObjectStore");
                alert("Completely removed all data.");
            } catch (error) {
                alert("Error: ", error);
            }
        });

        $('#look').on('click', async function () {
            const data = await getAllData(fileDb, "fileObjectStore");
            console.log("받은 데이터:", data);
        });

    });
}

function getAllData(db, storeName) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(storeName, "readonly");
        const store = transaction.objectStore(storeName);
        const request = store.getAll();

        request.onsuccess = function(event) {
            resolve(event.target.result);
        };

        request.onerror = function(event) {
            reject(event.target.error);
        };
    });
}

function deleteAllData(db, storeName) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(storeName, "readwrite");
        const store = transaction.objectStore(storeName);

        const request = store.clear();

        request.onsuccess = function(event) {
            resolve(event.target.result);
        };

        request.onerror = function(event) {
            reject(event.target.error);
        };
    });
}

async function fetchDataFromServer(apiUrl, type) {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const parsedData = Object.keys(data.data).map(key => ({
            id: data.data[key].doc_id,
            ...data.data[key]
        }));

        await updateIndexedDB(parsedData, type);
    } catch (error) {
        console.error("Error fetching data: ", error.message);
    }
}

async function updateIndexedDB(data, type) {
    const db = (type === 'file') ? fileDb : companyDb;
    const storeName = (type === 'file') ? "fileObjectStore" : "companyObjectStore";

    const transaction = db.transaction([storeName], "readwrite");
    const objectStore = transaction.objectStore(storeName);

    for (const item of data) {
        await new Promise((resolve, reject) => {
            const existingRequest = objectStore.get(item.id);

            existingRequest.onsuccess = function(event) {
                const existingItem = event.target.result;
                if (existingItem) {
                    if (JSON.stringify(existingItem) !== JSON.stringify(item)) {
                        const updateRequest = objectStore.put(item);
                        updateRequest.onsuccess = function() {
                            console.log("Item updated: ", item);
                            resolve();
                        };
                    } else {
                        console.log("No changes for item: ", item);
                        resolve();
                    }
                } else {
                    const addRequest = objectStore.put(item);
                    addRequest.onsuccess = function() {
                        console.log("Item added: ", item);
                        resolve();
                    };
                }
            };

            existingRequest.onerror = function(event) {
                console.error("Error getting existing item: ", event.target.error);
                reject(event.target.error);
            };
        });
    }

    transaction.oncomplete = function() {
        console.log("Transaction completed: database modification finished.");
    };

    transaction.onerror = function(event) {
        console.error("Transaction error: ", event.target.error);
    };
}


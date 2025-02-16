async function fetchFromOpenAI(AImodel, payload) {
    const apiKey = 'YOUR_OPENAI_API_KEY';

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: AImodel, // gpt-4o-mini
            messages: [{ role: 'user', content: payload }],
            temperature: 0.7
        })
    });

    if (!response.ok) {
        const errorDetails = await response.json();
        console.error('Error:', errorDetails);
        return;
    }

    const result = await response.json();
    console.log('Response:', result);
    alert(`Response: ${result.choices[0].message.content}`);
}

function limitText(text, limit) {
    if (text == null) return "...";
    if (Array.isArray(text)) {
        text = text.join(', ').trim(); 
    }
    if (typeof text !== "string") return "..."; 

    return text.length > limit ? text.substring(0, limit) + '...' : text;
}

async function downloadFile(fileName) {
    $.ajax({
        url: '/download/' + encodeURIComponent(fileName),
        method: 'GET',
        xhrFields: {
            responseType: 'blob' 
        },
        success: function(data) {
            var downloadUrl = window.URL.createObjectURL(data);
            var a = document.createElement('a');
            a.href = downloadUrl;
            a.download = fileName; 
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a); 
        },
        error: function(xhr, status, error) {
            alert('파일 다운로드 실패: ' + error);
        }
    });
}

function editField(fieldId, isTextarea) {
    if (isEditing) return;
    isEditing = true;

    let originalText = $('#' + fieldId).html().replace(/<br\s*\/?>/gi, '\n');

    if (originalText.trim() === '***') originalText = '';

    let inputField;
    
    if (isTextarea) {
        inputField = $('<textarea class="form-control" rows="15" style="font-size: 10px;">' + originalText + '</textarea>');
    } else {
        inputField = $('<input type="text" class="form-control" value="' + originalText + '" style="font-size: 10px;" />');
    }

    $('#' + fieldId).empty().append(inputField);

    inputField.focus();

    inputField.on('blur', function() {
        let updatedText = $(this).val();
        if (updatedText.trim() === '') {
            $('#' + fieldId).html('***');
        } else {
            $('#' + fieldId).html(updatedText.replace(/\n/g, '<br>'));
        }
        isEditing = false;
    });

    inputField.on('keypress', function(event) {
        if (event.which === 13) { 
            event.preventDefault();

            const currentValue = $(this).val();
            $(this).val(currentValue + '\n'); 
        }
    });
}

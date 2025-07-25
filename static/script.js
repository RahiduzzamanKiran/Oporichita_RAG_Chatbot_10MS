document.getElementById('ask-btn').addEventListener('click', async () => {
    const queryInput = document.getElementById('query-input');
    const answerOutput = document.getElementById('answer-output');
    const query = queryInput.value.trim();

    if (!query) {
        answerOutput.textContent = 'প্রশ্নটি খালি রাখা যাবে না।';
        return;
    }

    answerOutput.textContent = '⌛ উত্তর আসছে... দয়া করে অপেক্ষা করুন।';

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query})
        });

        if (!response.ok) {
            answerOutput.textContent = 'সিস্টেমে সমস্যা হয়েছে, পরে আবার চেষ্টা করুন।';
            return;
        }

        const data = await response.json();
        answerOutput.textContent = data.answer || 'কোন উত্তর পাওয়া যায়নি।';
    } catch (error) {
        answerOutput.textContent = 'একটি ত্রুটি ঘটেছে: ' + error.message;
    }
});

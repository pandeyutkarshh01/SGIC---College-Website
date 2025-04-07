function printPage() {
    document.getElementById('print-section').style.display = 'block';
    document.getElementById('form-section').style.display = 'none';
    window.print();
    document.getElementById('form-section').style.display = 'block';
    document.getElementById('print-section').style.display = 'none';
}
document.addEventListener("DOMContentLoaded", function() {
    const priceInput = document.getElementById("id_price");
    const taxInput = document.getElementById("id_customs_tax_estimate");
    const totalInput = document.getElementById("id_total_price");

    function updateTotal() {
        const price = parseFloat(priceInput.value) || 0;
        const tax = parseFloat(taxInput.value) || 0;
        totalInput.value = (price + tax).toFixed(2);
    }

    priceInput.addEventListener("input", updateTotal);
    taxInput.addEventListener("input", updateTotal);
});

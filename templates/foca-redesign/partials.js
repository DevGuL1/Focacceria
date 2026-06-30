// პატარა helper: WhatsApp ტექსტის გენერაცია (პროდუქტის სახელით)
// შენიშვნა: ეს დემო-საიტია; რეალურ საიტში შეგიძლია პროდუქტის ID/ვარიაციები დაამატო.

function waLink(text) {
  const phone = '995598800045';
  const msg = encodeURIComponent(text);
  return `https://wa.me/${phone}?text=${msg}`;
}


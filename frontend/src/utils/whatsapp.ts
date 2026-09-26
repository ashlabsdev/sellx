function normalizePhoneNumber(
  phone: string,
): string {
  let cleaned = phone.replace(
    /[^0-9]/g,
    '',
  )

  // SellX currently assumes Indian phone
  // numbers when only 10 digits are stored.
  if (cleaned.length === 10) {
    cleaned = `91${cleaned}`
  }

  return cleaned
}


export function buildWhatsAppUrl(
  phone: string,
  productName: string,
  productUrl: string,
): string {
  const cleanPhone =
    normalizePhoneNumber(phone)

  const message = [
    `Hi, I'm interested in the ${productName} listed on SellX.`,
    '',
    `Product: ${productName}`,
    `Link: ${productUrl}`,
    '',
    'Is it still available?',
  ].join('\n')

  return (
    `https://wa.me/${cleanPhone}` +
    `?text=${encodeURIComponent(message)}`
  )
}
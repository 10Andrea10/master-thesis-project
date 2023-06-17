export function hexStringLittleToBigEndian(hexString: string): string {
  let result = '';
  for (let i = 0; i < hexString.length; i += 2) {
    result = hexString.substring(i, i + 2) + result;
  }
  return result;
}

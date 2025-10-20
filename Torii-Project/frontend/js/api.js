// Simple API helper; adjust base as needed
export async function postForm(url, formData){
  const res = await fetch(url, { method:'POST', body: formData });
  const text = await res.text();
  return text;
}

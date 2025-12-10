import React, { useState } from "react";
import API from "../api";

export default function NewAnalysis(){
  const [url, setUrl] = useState("");
  const [files, setFiles] = useState<FileList | null>(null);
  const [created, setCreated] = useState<number | null>(null);

  async function handleSubmit(e: React.FormEvent){
    e.preventDefault();
    const form = new FormData();
    if(url) form.append("source_url", url);
    if(files){
      Array.from(files).forEach(f => form.append("files", f));
    }
    const res = await API.post("/analyses", form, { headers: { "Content-Type": "multipart/form-data" }});
    setCreated(res.data.id);
  }

  return (
    <div>
      <h2>Nouvelle analyse</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>URL de l'annonce</label><br/>
          <input value={url} onChange={e=>setUrl(e.target.value)} style={{width:600}} placeholder="https://..." />
        </div>
        <div>
          <label>Photos (optionnel)</label><br/>
          <input type="file" multiple onChange={(e)=>setFiles(e.target.files)} />
        </div>
        <button type="submit">Lancer l'analyse</button>
      </form>

      {created && <p>Analyse lancée — ID: {created} — <a href={`http://localhost:8000/analyses/${created}`}>Voir résultat (API)</a></p>}
    </div>
  )
}

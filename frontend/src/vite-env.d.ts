// src/vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_BASE_URL: string;
    readonly VITE_USER_ID: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
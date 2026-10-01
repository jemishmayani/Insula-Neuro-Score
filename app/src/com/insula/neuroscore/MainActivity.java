package com.insula.neuroscore;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * Thin native shell. The app UI and all score content are local files served from a private
 * origin (https://app.insula.local/) so pages can fetch JSON content without network access.
 * Content override: a file at <filesDir>/content-override/<path> replaces the bundled
 * assets/content/<path>, so individual score files can be updated without changing app code.
 */
public class MainActivity extends Activity {
    static final String HOST = "app.insula.local";
    static final String ORIGIN = "https://" + HOST + "/";
    private WebView web;

    public class Bridge {
        @JavascriptInterface public void copy(String text) {
            ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            if (cm != null) cm.setPrimaryClip(ClipData.newPlainText("Insula Neuro Score", text));
        }
        @JavascriptInterface public void share(String text) {
            Intent i = new Intent(Intent.ACTION_SEND);
            i.setType("text/plain");
            i.putExtra(Intent.EXTRA_TEXT, text);
            startActivity(Intent.createChooser(i, "Share result"));
        }
        @JavascriptInterface public void openUrl(String url) {
            if (url == null || !(url.startsWith("https://") || url.startsWith("http://"))) return;
            try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); }
            catch (Exception e) { runOnUiThread(new Runnable() { public void run() {
                Toast.makeText(MainActivity.this, "No browser available", Toast.LENGTH_SHORT).show(); }}); }
        }
        @JavascriptInterface public void setSystemBars(final boolean dark) {
            runOnUiThread(new Runnable() { public void run() { applyBars(dark); }});
        }
    }

    private void applyBars(boolean dark) {
        Window w = getWindow();
        int c = Color.parseColor(dark ? "#0D181C" : "#F5F8F9");
        w.setStatusBarColor(c);
        w.setNavigationBarColor(dark ? Color.parseColor("#13232A") : Color.WHITE);
        int flags = 0;
        if (!dark) {
            flags |= View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
            if (Build.VERSION.SDK_INT >= 26) flags |= 0x00000010; // SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
        }
        w.getDecorView().setSystemUiVisibility(flags);
        if (web != null) web.setBackgroundColor(c);
    }

    private boolean systemDark() {
        return (getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;
    }

    private static String mime(String path) {
        if (path.endsWith(".html")) return "text/html";
        if (path.endsWith(".js")) return "application/javascript";
        if (path.endsWith(".css")) return "text/css";
        if (path.endsWith(".json")) return "application/json";
        if (path.endsWith(".woff2")) return "font/woff2";
        if (path.endsWith(".png")) return "image/png";
        if (path.endsWith(".svg")) return "image/svg+xml";
        return "application/octet-stream";
    }

    private WebResourceResponse serve(Uri uri) {
        String path = uri.getPath();
        if (path == null || path.equals("/") || path.isEmpty()) path = "/index.html";
        path = path.substring(1);
        if (path.contains("..")) return notFound();
        Map<String, String> headers = new HashMap<String, String>();
        headers.put("Cache-Control", "no-cache");
        try {
            InputStream in = null;
            if (path.startsWith("content/")) {
                File f = new File(new File(getFilesDir(), "content-override"), path.substring("content/".length()));
                if (f.isFile()) in = new FileInputStream(f);
            }
            if (in == null) in = getAssets().open(path);
            return new WebResourceResponse(mime(path), "utf-8", 200, "OK", headers, in);
        } catch (Exception e) {
            return notFound();
        }
    }
    private WebResourceResponse notFound() {
        return new WebResourceResponse("text/plain", "utf-8", 404, "Not Found", new HashMap<String, String>(),
                new ByteArrayInputStream(new byte[0]));
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        applyBars(systemDark());
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setSupportZoom(false);
        s.setTextZoom(Math.round(getResources().getConfiguration().fontScale * 100)); // honour system text size
        web.addJavascriptInterface(new Bridge(), "Android");
        web.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest req) {
                Uri u = req.getUrl();
                if (HOST.equals(u.getHost())) return serve(u);
                return notFound(); // offline-first: no other network requests
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, String url) {
                Uri u = Uri.parse(url);
                if (HOST.equals(u.getHost())) return false;
                new Bridge().openUrl(url);
                return true;
            }
        });
        setContentView(web);
        if (savedInstanceState != null) web.restoreState(savedInstanceState);
        else web.loadUrl(ORIGIN + "index.html");
    }

    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); web.saveState(out); }

    @Override
    public void onConfigurationChanged(Configuration c) {
        super.onConfigurationChanged(c);
        web.getSettings().setTextZoom(Math.round(c.fontScale * 100));
        web.evaluateJavascript("window.dispatchEvent(new Event('ins-config'))", null);
    }

    @Override
    public void onBackPressed() {
        web.evaluateJavascript("window.handleBack ? window.handleBack() : false", new ValueCallback<String>() {
            public void onReceiveValue(String handled) {
                if (!"true".equals(handled)) MainActivity.super.onBackPressed();
            }
        });
    }
}

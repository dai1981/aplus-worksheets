<?php
/* Quiz together: enter the 6-digit code shown on the host's screen (/worksheets/join/) */
page_head(array(
    'title' => 'Join a Quiz with a Code | ' . SITE_NAME,
    'desc' => 'Type the 6-digit code from the host\'s screen to join the quiz with your class or friends.',
    'canonical' => 'join/',
    'noindex' => true,
));
site_header(array());
?>
<main class="sn-wrap">
<form class="mq-join-f" id="mqf" autocomplete="off">
  <h1>Join a quiz</h1>
  <p>Type the 6-digit code on the host's screen.</p>
  <input id="mqc" inputmode="numeric" pattern="[0-9 ]*" maxlength="7" placeholder="000000" aria-label="Code">
  <button id="mqb" type="submit">Join</button>
  <p class="mq-join-e" id="mqe" role="alert"></p>
  <p class="mq-join-n">You can also scan the QR code with a phone camera.</p>
</form>
</main>
<style>
.mq-join-f{max-width:420px;margin:28px auto 40px;border:4px solid #006633;border-radius:18px;padding:22px 18px;text-align:center;background:#fff}
.mq-join-f h1{margin:0 0 6px}
.mq-join-f input{display:block;width:100%;box-sizing:border-box;font-size:40px;font-weight:800;letter-spacing:.2em;text-align:center;padding:10px 6px;border:3px solid #cfc7ba;border-radius:14px;font-family:inherit}
.mq-join-f input:focus{outline:0;border-color:#006633}
.mq-join-f button{display:block;width:100%;margin:14px 0 0;border:0;border-radius:999px;background:#006633;color:#fff;font-size:20px;font-weight:800;padding:13px;cursor:pointer;font-family:inherit}
.mq-join-f button:disabled{background:#b9c7be}
.mq-join-e{color:#c0392b;font-weight:700;min-height:1.6em;margin:10px 0 0}
.mq-join-n{font-size:14px;color:#6b6259}
</style>
<script>
(function () {
  var f = document.getElementById("mqf"), c = document.getElementById("mqc"),
      b = document.getElementById("mqb"), e = document.getElementById("mqe");
  var q = /[?&]c=(\d{6})/.exec(location.search);
  if (q) c.value = q[1];
  c.focus();
  f.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var v = c.value.replace(/\D/g, "");
    if (v.length !== 6) { e.textContent = "Please type all 6 numbers."; return; }
    b.disabled = true; e.textContent = "";
    fetch("<?= url('api/mq.php') ?>", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ a: "find", c: v }), cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j && j.pg) { location.href = j.pg + "?mq=" + j.c; return; }
        b.disabled = false;
        e.textContent = "No quiz uses this code. Please check it.";
      })
      .catch(function () { b.disabled = false; e.textContent = "Can't connect. Please try again."; });
  });
})();
</script>
<?php site_footer('en', false); ?>
</body>
</html>

/* Bhagyank Calculator - calculators for all pages (plain JavaScript, no libraries). */
;(function () {
  'use strict'

  /*__DATA__*/

  var MONTHS = {
    en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    hi: ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'],
  }

  var TEXT = {
    en: {
      missing: 'Please select your full date of birth.',
      invalid: 'This date does not exist. Please check the day and month.',
      badge: 'Bhagyank',
      yourNumber: 'Your Destiny Number is',
      planet: 'Ruling Planet',
      mulank: 'Mulank',
      strengths: 'Strengths',
      challenges: 'Watch-Outs',
      careers: 'Ideal Careers',
      lucky: 'Lucky Colors &amp; Days',
      calc: function (t, b) {
        return 'Calculation: all digits of your date of birth add up to ' + t + ', which reduces to Bhagyank ' + b + '.'
      },
      more: function (b) { return 'Full Bhagyank ' + b + ' meaning' },
      loshu: 'Make my Lo Shu Grid',
      shareBtn: 'Share on WhatsApp',
      share: function (b, title) {
        return 'My Bhagyank is ' + b + ' (' + title + '). Find yours free: https://www.bhagyank-calculator.online/'
      },
    },
    hi: {
      missing: 'कृपया अपनी पूरी जन्मतिथि चुनें।',
      invalid: 'यह तारीख़ मौजूद नहीं है। कृपया दिन और महीना जाँचें।',
      badge: 'भाग्यांक',
      yourNumber: 'आपका भाग्यांक है',
      planet: 'स्वामी ग्रह',
      mulank: 'मूलांक',
      strengths: 'खूबियाँ',
      challenges: 'सावधानियाँ',
      careers: 'उपयुक्त करियर',
      lucky: 'शुभ रंग और दिन',
      calc: function (t, b) {
        return 'गणना: आपकी जन्मतिथि के सभी अंकों का योग ' + t + ' है, जिसे एक अंक में बदलने पर भाग्यांक ' + b + ' आता है।'
      },
      more: function (b) { return 'भाग्यांक ' + b + ' का पूरा अर्थ' },
      loshu: 'लो शू ग्रिड बनाएँ',
      shareBtn: 'WhatsApp पर शेयर करें',
      share: function (b, title) {
        return 'मेरा भाग्यांक ' + b + ' (' + title + ') है। अपना भाग्यांक मुफ़्त में जानें: https://www.bhagyank-calculator.online/hi'
      },
    },
  }

  var ICON =
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l1.9 5.6L19.5 9.5l-5.6 1.9L12 17l-1.9-5.6L4.5 9.5l5.6-1.9L12 2z" fill="currentColor"/></svg>'

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    })
  }

  function reduce(n) {
    n = Math.abs(n)
    while (n > 9) {
      n = String(n).split('').reduce(function (s, d) { return s + Number(d) }, 0)
    }
    return n
  }

  function digitSum(str) {
    return String(str).split('').reduce(function (s, d) { return s + (Number(d) || 0) }, 0)
  }

  function daysInMonth(month, year) {
    // Before a year is chosen, allow 29 Feb (leap year).
    return new Date(year || 2000, month, 0).getDate()
  }

  function scrollTo(el) {
    if (!el) return
    requestAnimationFrame(function () {
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    })
  }

  function fill(select, values, labels) {
    var keep = select.value
    var first = select.options[0]
    select.innerHTML = ''
    select.appendChild(first)
    values.forEach(function (v, i) {
      var o = document.createElement('option')
      o.value = v
      o.textContent = labels ? labels[i] : v
      select.appendChild(o)
    })
    if (keep && values.map(String).indexOf(keep) !== -1) select.value = keep
  }

  function range(a, b) {
    var out = []
    for (var i = a; i <= b; i++) out.push(i)
    return out
  }

  /* Day / month / year selects that only offer real dates. */
  function setupDob(root, lang) {
    var day = root.querySelector('[data-dob="day"]')
    var month = root.querySelector('[data-dob="month"]')
    var year = root.querySelector('[data-dob="year"]')
    fill(month, range(1, 12), MONTHS[lang])
    if (year) {
      var now = new Date().getFullYear()
      fill(year, range(now - 119, now).reverse())
    }
    function updateDays() {
      var max = month.value ? daysInMonth(Number(month.value), year ? Number(year.value) : 0) : 31
      fill(day, range(1, max))
    }
    updateDays()
    month.addEventListener('change', updateDays)
    if (year) year.addEventListener('change', updateDays)
    return { day: day, month: month, year: year }
  }

  function showError(form, msg) {
    var p = form.querySelector('.error')
    p.textContent = msg || ''
    p.hidden = !msg
  }

  function list(items) {
    return '<ul>' + items.map(function (s) { return '<li>' + esc(s) + '</li>' }).join('') + '</ul>'
  }

  /* ---------------- Bhagyank ---------------- */
  function bhagyank(root) {
    var lang = root.getAttribute('data-lang') === 'hi' ? 'hi' : 'en'
    var t = TEXT[lang]
    var form = root.querySelector('form')
    var out = root.querySelector('.result')
    var f = setupDob(root, lang)

    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!f.day.value || !f.month.value || !f.year.value) return showError(form, t.missing)
      var d = Number(f.day.value), m = Number(f.month.value), y = Number(f.year.value)
      if (d > daysInMonth(m, y)) return showError(form, t.invalid)
      showError(form, '')

      var total = digitSum('' + d + m + y)
      var b = reduce(total)
      var mul = reduce(d)
      var en = DATA.en[b]
      var info = lang === 'hi' ? DATA.hi[b] : en
      var planet = lang === 'hi' ? info.planet : en.planet + ' (' + en.planetHindi + ')'

      out.innerHTML =
        '<div class="card result-card">' +
        '<div class="result-top"><div class="circle"><span>' + b + '</span><small>' + t.badge + '</small></div>' +
        '<div><p class="muted small">' + t.yourNumber + '</p><h3 class="result-title">' + b + ' - ' + esc(info.title) + '</h3>' +
        '<div class="chips"><span class="chip">' + t.planet + ': ' + esc(planet) + '</span>' +
        '<span class="chip">' + t.mulank + ': ' + mul + '</span></div></div></div>' +
        '<p class="result-summary">' + esc(info.summary) + '</p>' +
        '<div class="info-grid">' +
        '<div class="info"><h4>' + ICON + ' ' + t.strengths + '</h4>' + list(info.strengths) + '</div>' +
        '<div class="info"><h4 class="accent">' + ICON + ' ' + t.challenges + '</h4>' + list(info.challenges) + '</div>' +
        '<div class="info"><h4>' + ICON + ' ' + t.careers + '</h4><p>' + esc(info.career) + '</p></div>' +
        '<div class="info"><h4>' + ICON + ' ' + t.lucky + '</h4><p>' + esc(info.luckyColors.join(', ')) + '<br>' +
        esc(info.luckyDays.join(', ')) + '</p></div>' +
        '</div><p class="xs muted calc-note">' + t.calc(total, b) + '</p>' +
        '<div class="result-actions">' +
        '<a class="btn inline" href="' + (lang === 'hi' ? '/hi/bhagyank/' : '/bhagyank/') + b + '">' + t.more(b) + '</a>' +
        '<a class="btn inline ghost" href="/lo-shu-grid-calculator">' + t.loshu + '</a>' +
        '<a class="btn inline ghost" target="_blank" rel="noopener" href="https://wa.me/?text=' +
        encodeURIComponent(t.share(b, info.title)) + '">' + t.shareBtn + '</a>' +
        '</div></div>'
      scrollTo(out)
    })
  }

  /* ---------------- Lo Shu grid ---------------- */
  var LS_ORDER = [4, 9, 2, 3, 5, 7, 8, 1, 6]
  var LS_PLANES = [
    ['Mental plane', [4, 9, 2]], ['Emotional plane', [3, 5, 7]], ['Practical plane', [8, 1, 6]],
    ['Thought plane', [4, 3, 8]], ['Will plane', [9, 5, 1]], ['Action plane', [2, 7, 6]],
    ['Golden Yog', [4, 5, 6]], ['Silver Yog', [2, 5, 8]],
  ]
  var LS_AREA = {
    1: 'communication and career', 2: 'feelings and intuition', 3: 'learning and imagination',
    4: 'order and hard work', 5: 'balance and focus', 6: 'family, home and comforts',
    7: 'inner growth and luck', 8: 'money handling and patience', 9: 'energy and ambition',
  }

  function loshu(root) {
    var form = root.querySelector('form')
    var out = root.querySelector('.result')
    var f = setupDob(root, 'en')
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!f.day.value || !f.month.value || !f.year.value) return showError(form, 'Please select your full date of birth.')
      var d = Number(f.day.value), m = Number(f.month.value), y = Number(f.year.value)
      if (d > daysInMonth(m, y)) return showError(form, 'This date does not exist. Please check the day and month.')
      showError(form, '')
      var digits = ('' + d + m + y).split('').map(Number).filter(function (x) { return x > 0 })
      var mul = reduce(d)
      var bhag = reduce(digitSum('' + d + m + y))
      var all = digits.concat([mul, bhag])
      var count = {}
      all.forEach(function (x) { count[x] = (count[x] || 0) + 1 })
      var cells = LS_ORDER.map(function (k) {
        var v = count[k] ? new Array(count[k] + 1).join(String(k)) : ''
        return '<div class="ls-cell' + (v ? '' : ' ls-empty') + '"><span class="ls-pos">' + k + '</span><span class="ls-val">' + v + '</span></div>'
      }).join('')
      var missing = [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(function (k) { return !count[k] })
      var repeated = [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(function (k) { return count[k] > 1 })
      var planes = LS_PLANES.filter(function (p) { return p[1].every(function (k) { return count[k] }) })
      out.innerHTML =
        '<div class="card result-card">' +
        '<div class="ls-result"><div class="ls-grid" aria-label="Your Lo Shu Grid">' + cells + '</div>' +
        '<div><p class="muted small">Your Lo Shu Grid</p><h3 class="result-title">' + d + '-' + m + '-' + y + '</h3>' +
        '<div class="chips"><span class="chip">Mulank: ' + mul + '</span><span class="chip">Bhagyank: ' + bhag + '</span></div>' +
        '<p class="xs muted calc-note">Digits used: ' + digits.join(', ') + ' + Mulank ' + mul + ' + Bhagyank ' + bhag + ' (zeros are left out)</p></div></div>' +
        '<div class="info-grid">' +
        '<div class="info"><h4>Complete planes</h4>' + (planes.length ? list(planes.map(function (p) { return p[0] + ' (' + p[1].join('-') + ')' })) : '<p>No complete plane - that is very common.</p>') + '</div>' +
        '<div class="info"><h4>Repeated numbers</h4>' + (repeated.length ? list(repeated.map(function (k) { return k + ' x' + count[k] + ' - strong ' + LS_AREA[k] })) : '<p>None</p>') + '</div>' +
        '<div class="info" style="grid-column:1/-1"><h4 class="accent">Missing numbers</h4>' + (missing.length ? list(missing.map(function (k) { return k + ' - may need effort in ' + LS_AREA[k] })) : '<p>None - every number is present.</p>') + '</div>' +
        '</div>' +
        '<div class="result-actions"><a class="btn inline" href="/bhagyank/' + bhag + '">Read Bhagyank ' + bhag + ' meaning</a></div>' +
        '</div>'
      scrollTo(out)
    })
  }

  /* ---------------- Moolank ---------------- */
  function moolank(root) {
    var form = root.querySelector('form')
    var out = root.querySelector('.result')
    var f = setupDob(root, 'en')
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!f.day.value || !f.month.value) return showError(form, 'Please select your birth day and month.')
      var d = Number(f.day.value)
      if (d > daysInMonth(Number(f.month.value), 0)) return showError(form, 'This date does not exist. Please check the day and month.')
      showError(form, '')
      var m = reduce(d)
      var info = DATA.en[m]
      out.innerHTML =
        '<div class="card result-card">' +
        '<div class="result-top"><div class="circle"><span>' + m + '</span><small>Moolank</small></div>' +
        '<div><p class="muted small">Your Birth Number is</p><h3 class="result-title">' + m + ' - ' + esc(info.title) + '</h3>' +
        '<div class="chips"><span class="chip">Ruling Planet: ' + esc(info.planet + ' (' + info.planetHindi + ')') + '</span></div></div></div>' +
        '<p class="result-summary">' + esc(info.summary) + '</p>' +
        '<div class="info-grid">' +
        '<div class="info"><h4>Personality strengths</h4>' + list(info.strengths) + '</div>' +
        '<div class="info"><h4 class="accent">Suitable careers</h4><p>' + esc(info.career) + '</p></div>' +
        '</div><p class="xs muted calc-note">Your Moolank is calculated by reducing your birth day, ' + d + ', to a single digit.</p></div>'
      scrollTo(out)
    })
  }

  /* ---------------- Namank ---------------- */
  var LETTERS = {
    a: 1, i: 1, j: 1, q: 1, y: 1, b: 2, k: 2, r: 2, c: 3, g: 3, l: 3, s: 3, d: 4, m: 4, t: 4,
    e: 5, h: 5, n: 5, x: 5, u: 6, v: 6, w: 6, o: 7, z: 7, f: 8, p: 8,
  }
  var NAMANK = {
    1: ['The Leader', 'Independent, ambitious and confident energy.'],
    2: ['The Diplomat', 'Cooperative, intuitive and emotionally aware energy.'],
    3: ['The Creator', 'Expressive, optimistic and socially magnetic energy.'],
    4: ['The Builder', 'Practical, disciplined and dependable energy.'],
    5: ['The Explorer', 'Adaptable, curious and freedom-loving energy.'],
    6: ['The Nurturer', 'Caring, artistic and harmony-seeking energy.'],
    7: ['The Seeker', 'Thoughtful, spiritual and analytical energy.'],
    8: ['The Achiever', 'Organised, determined and results-focused energy.'],
    9: ['The Humanitarian', 'Compassionate, courageous and generous energy.'],
  }

  function namank(root) {
    var form = root.querySelector('form')
    var input = form.querySelector('input')
    var btn = form.querySelector('button')
    var out = root.querySelector('.tool-result')
    input.addEventListener('input', function () {
      var clean = input.value.replace(/[^a-zA-Z ]/g, '')
      if (clean !== input.value) input.value = clean
      btn.disabled = !clean.trim()
    })
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      var name = input.value.trim()
      var total = name.toLowerCase().split('').reduce(function (s, c) { return s + (LETTERS[c] || 0) }, 0)
      if (!total) return
      var n = reduce(total)
      out.innerHTML =
        '<div class="tool-out"><p class="eyebrow">Your Namank</p><p class="big-num">' + n + '</p>' +
        '<p class="result-title">' + NAMANK[n][0] + '</p><p class="muted">' + NAMANK[n][1] + '</p>' +
        '<p class="small muted">Name analysed: ' + esc(name) + '</p>' +
        '<button type="button" class="text-btn" data-reset>Try another name</button></div>'
      out.querySelector('[data-reset]').addEventListener('click', function () {
        input.value = ''
        btn.disabled = true
        out.innerHTML = ''
        input.focus()
      })
      scrollTo(out)
    })
  }

  /* ---------------- Gemstone ---------------- */
  var STONES = {
    1: ['Ruby', 'माणिक्य', 'Sun', 'Confidence, leadership and vitality', 'Red'],
    2: ['Pearl', 'मोती', 'Moon', 'Emotional balance and calmness', 'White'],
    3: ['Yellow Sapphire', 'पुखराज', 'Jupiter', 'Wisdom, growth and prosperity', 'Yellow'],
    4: ['Hessonite', 'गोमेद', 'Rahu', 'Focus, courage and stability', 'Honey brown'],
    5: ['Emerald', 'पन्ना', 'Mercury', 'Communication, learning and creativity', 'Green'],
    6: ['Diamond', 'हीरा', 'Venus', 'Love, beauty and harmony', 'White'],
    7: ["Cat's Eye", 'लहसुनिया', 'Ketu', 'Intuition, protection and spirituality', 'Greenish gold'],
    8: ['Blue Sapphire', 'नीलम', 'Saturn', 'Discipline, patience and progress', 'Blue'],
    9: ['Red Coral', 'मूंगा', 'Mars', 'Energy, courage and determination', 'Red-orange'],
  }

  function gemstone(root) {
    var form = root.querySelector('form')
    var input = form.querySelector('input')
    var btn = form.querySelector('button')
    var out = root.querySelector('.tool-result')
    input.max = new Date().toISOString().split('T')[0]
    input.addEventListener('input', function () { btn.disabled = !input.value })
    input.addEventListener('change', function () { btn.disabled = !input.value })
    form.addEventListener('submit', function (ev) {
      ev.preventDefault()
      if (!input.value) return
      var n = reduce(Number(input.value.split('-')[2]))
      var s = STONES[n]
      out.innerHTML =
        '<div class="tool-out"><p class="eyebrow">Your recommended gemstone</p>' +
        '<p class="result-title big">' + esc(s[0]) + '</p><p class="muted">' + s[1] + ' · Gemstone for Number ' + n + '</p>' +
        '<div class="stats"><div><p class="xs muted">Ruling planet</p><p>' + s[2] + '</p></div>' +
        '<div><p class="xs muted">Traditional benefit</p><p>' + s[3] + '</p></div>' +
        '<div><p class="xs muted">Associated color</p><p>' + s[4] + '</p></div></div>' +
        '<button type="button" class="text-btn" data-reset>Try another date</button></div>'
      out.querySelector('[data-reset]').addEventListener('click', function () {
        input.value = ''
        btn.disabled = true
        out.innerHTML = ''
      })
      scrollTo(out)
    })
  }

  var INIT = { bhagyank: bhagyank, moolank: moolank, namank: namank, gemstone: gemstone, loshu: loshu }

  document.querySelectorAll('[data-calc]').forEach(function (el) {
    var fn = INIT[el.getAttribute('data-calc')]
    if (fn) fn(el)
  })

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear()
  })
})()

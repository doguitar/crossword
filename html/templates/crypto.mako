<%inherit file="/base.mako"/>
<%namespace name="nav" file="/nav.mako"/>
<%block name="nav_block">
    ${nav.make_nav('crypto')}
</%block>
<script src="${base}js/crypto/rollups/sha3.js"></script>
<script type="text/javascript">
    $(document).ready(function(){
       $("input").keyup(function(){
          $(this).next().text(CryptoJS.SHA3($(this).val()).toString());
       });
    });
</script>
<input id="sha3" type="text" /><span></span>
<br>


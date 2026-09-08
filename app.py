import streamlit as st
import random

st.set_page_config(page_title="Jogo da Planilha Financeira", layout="wide")

# Configuração do Estado da Sessão
if "fase" not in st.session_state:
    st.session_state.fase = 1
if "gastos_classificados" not in st.session_state:
    st.session_state.gastos_classificados = {}
if "etapa_f3" not in st.session_state:
    st.session_state.etapa_f3 = 1
if "passos_f3" not in st.session_state:
    st.session_state.passos_f3 = []
if "opcoes_shuffled" not in st.session_state:
    st.session_state.opcoes_shuffled = None

RENDA_TOTAL = 3000.00
CATEGORIAS = {
    "Aluguel": {"tipo": "fixo", "valor": 1000.00, "pct": "33,3%", "emoji": "🏠"},
    "Alimentação": {"tipo": "variavel", "valor": 600.00, "pct": "20,0%", "emoji": "🛒"},
    "Transporte": {"tipo": "fixo", "valor": 300.00, "pct": "10,0%", "emoji": "🚗"},
    "Lazer": {"tipo": "variavel", "valor": 300.00, "pct": "10,0%", "emoji": "🏖️"},
    "Energia e Água": {"tipo": "variavel", "valor": 250.00, "pct": "8,3%", "emoji": "⚡"},
    "Compras Diversas": {"tipo": "variavel", "valor": 250.00, "pct": "8,3%", "emoji": "💳"},
    "Internet e Telefone": {"tipo": "fixo", "valor": 150.00, "pct": "5,0%", "emoji": "📱"},
}

# ==========================================
# FASE 1: RECONHECIMENTO DE PADRÕES
# ==========================================
if st.session_state.fase == 1:
    st.title("FASE 1: Classificação de Gastos")
    st.caption("Classifique as 7 categorias abaixo como FIXO (contratual) ou VARIÁVEL (ajustável).")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("💵 Renda", "R$ 3.000,00")
    col_m2.metric("📉 Despesas", "R$ 2.850,00")
    col_m3.metric("💰 Sobra Atual", "R$ 150,00")
    col_m4.metric("🎯 Meta Poupança", "R$ 200,00")

    st.markdown("---")
    cols = st.columns(len(CATEGORIAS))

    for idx, (nome, info) in enumerate(CATEGORIAS.items()):
        with cols[idx]:
            st.subheader(f"{info['emoji']} {nome}")
            st.write(f"**R$ {info['valor']:.2f}** ({info['pct']})")
            
            escolha = st.radio(
                "Tipo:", 
                ["Selecione...", "Fixo", "Variável"], 
                key=f"rad_{nome}"
            )
            
            if escolha != "Selecione...":
                st.session_state.gastos_classificados[nome] = "fixo" if escolha == "Fixo" else "variavel"

    st.markdown("---")

    # Verifica quantas categorias já foram selecionadas
    selecionados = len(st.session_state.gastos_classificados)
    st.info(f"Categorias respondidas: {selecionados} de {len(CATEGORIAS)}")

    if selecionados == len(CATEGORIAS):
        if st.button("✅ Validar Classificação e Avançar", use_container_width=True, type="primary"):
            erros = sum(1 for n, i in CATEGORIAS.items() if st.session_state.gastos_classificados.get(n) != i["tipo"])
            if erros == 0:
                st.success("Excelente! Todos os padrões foram identificados corretamente.")
                st.session_state.fase = 2
                st.rerun()
            else:
                st.error(f"Você errou {erros} categoria(s). Lembre-se: Energia/Água, Alimentação, Lazer e Compras são VARIÁVEIS. Aluguel, Transporte e Internet são FIXOS!")

# ==========================================
# FASE 2: SIMULADOR DE ORÇAMENTO
# ==========================================
elif st.session_state.fase == 2:
    st.title("FASE 2: Simulador de Ajuste Orçamentário")
    st.caption("Ajuste os valores dos Gastos Variáveis até atingir a meta de guardar R$ 200,00 por mês!")

    lazer = st.slider("🏖️ Lazer", 100, 300, 300, step=1)
    energia = st.slider("⚡ Energia e Água", 150, 250, 250, step=1)
    compras = st.slider("💳 Compras Diversas", 100, 250, 250, step=1)
    alimentacao = st.slider("🛒 Alimentação", 500, 600, 600, step=1)

    gastos_fixos = 1000 + 300 + 150
    gastos_var = lazer + energia + compras + alimentacao
    total_gastos = gastos_fixos + gastos_var
    economia = RENDA_TOTAL - total_gastos

    c1, c2, c3 = st.columns(3)
    c1.metric("📉 Total de Gastos", f"R$ {total_gastos:,.2f}")
    c2.metric("💰 Economia Guardada", f"R$ {economia:,.2f}", delta=f"{economia - 150:,.2f}")
    c3.metric("🎯 Meta", "R$ 200,00")

    if st.button("✅ APLICAR NOVO ORÇAMENTO", use_container_width=True, type="primary"):
        if economia >= 200:
            st.balloons()
            st.success(f"Parabéns! Você reajustou os gastos e agora guarda R$ {economia:.2f} por mês!")
            st.session_state.fase = 3
            st.rerun()
        else:
            st.warning(f"Sua economia é de R$ {economia:.2f}. Você precisa cortar mais R$ {200 - economia:.2f}!")

# ==========================================
# FASE 3: DECISÕES PRÁTICAS
# ==========================================
elif st.session_state.fase == 3:
    st.title("FASE 3: Planilha de Ações Financeiras")
    
    etapas_dados = {
        1: ("PASSO 1: REGISTRO DA RENDA LÍQUIDA", "O que você deve colocar no topo da sua planilha financeira no 1º dia do mês?", [
            ("Anotar apenas o valor exato da Renda Garantida (R$ 3.000,00) que já caiu na conta.", True, "Perfeito! Planejamento financeiro realista começa registrando o dinheiro que realmente existe."),
            ("Somar a renda real + o limite do cartão de crédito para ter 'mais dinheiro' na planilha.", False, "PEGADINHA: Limite do cartão é dívida potencial!"),
            ("Colocar um valor estimado com bônus e horas extras hipotéticas que você talvez ganhe.", False, "PEGADINHA: Contar com dinheiro incerto gera rombo no orçamento!"),
            ("Deixar a linha de receitas em branco e preencher só no final do mês.", False, "PEGADINHA: Sem saber a receita inicial, você não tem limite para controlar seus gastos!"),
            ("Registrar o salário bruto sem descontar impostos nem previdência.", False, "PEGADINHA: Você só pode planejar com o salário LÍQUIDO!")
        ]),
        2: ("PASSO 2: SEPARAÇÃO DOS COMPROMISSOS FIXOS", "Qual é a primeira atitude prática ao listar as contas a pagar?", [
            ("Criar um Bloco de Gastos Fixos (Aluguel, Transporte, Internet) com os valores exatos dos boletos.", True, "Exato! As contas contratuais são prioridades com datas de vencimento rígidas."),
            ("Deixar para registrar o Aluguel só no dia em que for pagar.", False, "PEGADINHA: Esconder contas fixas gera falsa sensação de dinheiro livre!"),
            ("Misturar contas fixas com compras de lazer na mesma lista.", False, "PEGADINHA: Se misturar, você não saberá o que pode cortar numa emergência!"),
            ("Ignorar o boleto de transporte e ir a pé quando o dinheiro acabar.", False, "PEGADINHA: O transporte é essencial para garantir sua renda!"),
            ("Colocar todas as contas fixas como opção negociável para cortar no fim do mês.", False, "PEGADINHA: Contas fixas contratadas geram multas e corte de serviço!")
        ]),
        3: ("PASSO 3: APLICAÇÃO DA REGRA 'PAGUE-SE PRIMEIRO'", "Qual a melhor forma de garantir a meta de economizar R$ 200,00?", [
            ("Tratar a Meta de R$ 200,00 como um boleto obrigatório e transferir para a Poupança no início do mês.", True, "Excelente! Quem se paga primeiro garante o futuro."),
            ("Esperar o fim do mês para ver se sobra R$ 200,00 e guardar o que restar.", False, "PEGADINHA: Quase nunca sobra dinheiro no final do mês sem compromisso prévio!"),
            ("Guardar R$ 200,00 em dinheiro vivo dentro de uma gaveta em casa.", False, "PEGADINHA: Dinheiro parado em casa perde valor para a inflação!"),
            ("Apostar os R$ 200,00 em jogos online para tentar dobrar o valor.", False, "PEGADINHA: Apostas são risco total de perda!"),
            ("Emprestar os R$ 200,00 para amigos visando receber com juros no mês seguinte.", False, "PEGADINHA: Empréstimos informais têm alto risco de inadimplência!")
        ]),
        4: ("PASSO 4: CÁLCULO DO TETO DE GASTOS VARIÁVEIS", "Como calcular quanto sobrou para passar o mês?", [
            ("Subtrair das Receitas (3.000) os Gastos Fixos (1.450) e a Meta (200), obtendo R$ 1.350.", True, "Correto! Esse é o seu Teto de Gastos Variáveis real."),
            ("Dividir toda a sua renda de R$ 3.000 em 30 dias sem descontar os boletos fixos.", False, "PEGADINHA: Faltará dinheiro para pagar o aluguel no vencimento!"),
            ("Considerar que todo o dinheiro restante na conta corrente pode ser gasto em lazer.", False, "PEGADINHA: Você precisa reservar dinheiro para a alimentação diária!"),
            ("Somar os gastos do mês passado e dobrar o limite para este mês.", False, "PEGADINHA: O teto é limitado pela sua renda real!"),
            ("Multiplicar a renda por 2 achando que o cartão de crédito é renda extra.", False, "PEGADINHA: Cartão não é renda, é pagamento adiantado com juros!")
        ]),
        5: ("PASSO 5: ANOTAÇÃO EM TEMPO REAL", "Como acompanhar o dinheiro que vai saindo no dia a dia?", [
            ("Anotar cada compra do cotidiano na planilha ou app no mesmo dia.", True, "Perfeito! O acompanhamento em tempo real evita surpresas."),
            ("Confiar apenas na memória e checar o extrato só de vez em quando.", False, "PEGADINHA: Pequenos gastos diários são os maiores vilões do orçamento!"),
            ("Juntar todas as notinhas de papel numa caixa e olhar só no final do ano.", False, "PEGADINHA: Olhar no final do ano não permite corrigir o mês atual!"),
            ("Anotar apenas as compras acima de R$ 100,00 e ignorar os gastos menores.", False, "PEGADINHA: Vários pequenos gastos somam centenas de reais!"),
            ("Pedir para outra pessoa gerenciar suas compras pessoais.", False, "PEGADINHA: O controle financeiro depende da sua conscientização!")
        ]),
        6: ("PASSO 6: ALERTA DE ESTOURO DO TETO", "Ao somar os gastos variáveis no meio do mês, o valor ultrapassou o limite. O que fazer?", [
            ("Acionar o alerta na planilha e tomar providências imediatas de corte para o restante do mês.", True, "Exato! O diagnóstico rápido permite corrigir a rota a tempo."),
            ("Ignorar a planilha e continuar gastando normalmente.", False, "PEGADINHA: Leva direto ao uso de cheque especial e juros!"),
            ("Usar o dinheiro guardado na meta de R$ 200 para cobrir o excesso de lazer.", False, "PEGADINHA: A reserva de futuro não deve ser gasta com supérfluos!"),
            ("Pegar um empréstimo rápido para cobrir os gastos variáveis.", False, "PEGADINHA: Empréstimo para consumo gera bola de neve!"),
            ("Apagar os registros antigos da planilha para o saldo parecer positivo.", False, "PEGADINHA: Maquiar a planilha não altera a conta bancária!")
        ]),
        7: ("PASSO 7: PLANO DE CORTE SELETIVO", "Para cortar despesas sem prejudicar a moradia, onde você atua?", [
            ("Focar cortes em Lazer, Restaurantes e Consumo de Energia.", True, "Muito bem! Reduzir custos flexíveis não gera multas nem perda de serviços."),
            ("Atrasar o pagamento do Aluguel para manter as saídas de fim de semana.", False, "PEGADINHA: Atrasar contas fixas gera multas e problemas graves!"),
            ("Cancelar a conta de energia e ficar no escuro para economizar.", False, "PEGADINHA: Reduzir custos não significa abdicar do básico!"),
            ("Vender os móveis de casa para pagar o cartão.", False, "PEGADINHA: Vender patrimônio para cobrir gastos rotineiros é insustentável!"),
            ("Parar de comprar comida e fazer refeições apenas quando for convidado.", False, "PEGADINHA: Alimentação é necessidade básica e essencial!")
        ]),
        8: ("PASSO 8: AJUSTE DE R$ 1 EM R$ 1", "Como recalibrar os limites das categorias na planilha de forma realista?", [
            ("Reduzir pequenos valores viáveis (ex: R$ 30 em lazer, R$ 20 em compras) até fechar a conta.", True, "Sensacional! Microajustes graduais são fáceis de cumprir."),
            ("Zerar completamente a categoria de Alimentação para economizar.", False, "PEGADINHA: Metas extremas são abandonadas logo no 2º dia!"),
            ("Reduzir aleatoriamente qualquer conta sem somar.", False, "PEGADINHA: Reajustes precisam de cálculo exato!"),
            ("Aumentar o limite de todas as categorias para não precisar cortar nada.", False, "PEGADINHA: Se aumentar os limites sem ter mais renda, a conta não fecha!"),
            ("Fixar o valor de todas as categorias em R$ 50 sem analisar as necessidades.", False, "PEGADINHA: Cada categoria possui custos mínimos reais!")
        ]),
        9: ("PASSO 9: CONSOLIDAÇÃO E FECHAMENTO", "No último dia do mês, qual a ação concreta de fechamento?", [
            ("Comparar a Planilha Prevista com o Extrato Real e comemorar os R$ 200,00 guardados.", True, "Perfeito! Fechar o ciclo valida todo o seu esforço."),
            ("Usar os R$ 200 economizados para fazer uma festa no último dia do mês.", False, "PEGADINHA: Esse dinheiro é sua reserva de futuro!"),
            ("Rasgar a planilha e não conferir se o dinheiro real bateu com os registros.", False, "PEGADINHA: A conferência garante que nenhum dinheiro se perdeu!"),
            ("Transferir o saldo restante para a conta de um estranho.", False, "PEGADINHA: O saldo positivo deve reforçar suas reservas!"),
            ("Reclamar que sobrou dinheiro e tentar gastar tudo antes da meia-noite.", False, "PEGADINHA: Sobrar dinheiro é a meta atingida!")
        ]),
        10: ("PASSO 10: DUPLICAÇÃO DA PLANILHA", "Como garantir que o hábito financeiro continue no mês seguinte?", [
            ("Duplicar a aba da planilha ajustada, atualizar as datas e iniciar o novo mês no controle.", True, "Parabéns! Você dominou o Roteiro Prático de Ações Orçamentárias! 🎉"),
            ("Apagar a planilha e voltar a gastar sem acompanhar nada.", False, "PEGADINHA: A consistência é o segredo para acumular patrimônio."),
            ("Mudar todas as regras financeiras e gastar o dobro no mês seguinte.", False, "PEGADINHA: O sucesso exige manter os bons hábitos!"),
            ("Esperar passar 6 meses para abrir a planilha novamente.", False, "PEGADINHA: O acompanhamento precisa ser mensal e contínuo."),
            ("Desistir do controle financeiro por achar que um mês já é suficiente.", False, "PEGADINHA: A saúde financeira é uma construção contínua!")
        ])
    }

    if st.session_state.etapa_f3 <= 10:
        tit, perg, ops_base = etapas_dados[st.session_state.etapa_f3]
        
        col_esq, col_dir = st.columns([1, 2])
        
        with col_esq:
            st.subheader("📌 Roteiro Construído")
            for p in st.session_state.passos_f3:
                st.info(p)

        with col_dir:
            st.subheader(f"Etapa {st.session_state.etapa_f3} de 10: {tit}")
            st.write(f"**{perg}**")

            if st.session_state.opcoes_shuffled is None:
                ops_shuffled = list(ops_base)
                random.shuffle(ops_shuffled)
                st.session_state.opcoes_shuffled = ops_shuffled
            else:
                ops_shuffled = st.session_state.opcoes_shuffled

            letras = ["A", "B", "C", "D", "E"]
            for i, (texto, eh_correta, exp) in enumerate(ops_shuffled):
                if st.button(f"{letras[i]}) {texto}", key=f"btn_f3_{st.session_state.etapa_f3}_{i}", use_container_width=True):
                    if eh_correta:
                        st.success(f"🎯 Correto! {exp}")
                        st.session_state.passos_f3.append(f"Passo {st.session_state.etapa_f3}: {texto}")
                        st.session_state.etapa_f3 += 1
                        st.session_state.opcoes_shuffled = None
                        st.rerun()
                    else:
                        st.error(f"⚠️ {exp}")
    else:
        st.session_state.fase = 4
        st.rerun()

# ==========================================
# RESUMO FINAL
# ==========================================
elif st.session_state.fase == 4:
    st.title("📊 MODELO FINAL: SUA PLANILHA DE AÇÃO FINANCEIRA")
    st.caption("Veja como ficou o seu orçamento na prática:")

    st.table([
        {"Categoria": "💵 Renda Total", "Tipo": "Receita", "Valor Inicial": "R$ 3.000,00", "Ação": "Entrada Integrativa", "Valor Final": "R$ 3.000,00"},
        {"Categoria": "🏠 Aluguel + Fixos", "Tipo": "Fixo Rígido", "Valor Inicial": "R$ 1.450,00", "Ação": "Manter Prioridade", "Valor Final": "R$ 1.450,00"},
        {"Categoria": "💰 Poupança (Meta)", "Tipo": "Reserva", "Valor Inicial": "R$ 150,00", "Ação": "+ R$ 50,00 (Aumento)", "Valor Final": "R$ 200,00"},
        {"Categoria": "🛒 Variáveis", "Tipo": "Flexível", "Valor Inicial": "R$ 1.400,00", "Ação": "- R$ 50,00 (Reajuste)", "Valor Final": "R$ 1.350,00"},
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.info("**🧩 Decomposição na Prática**\nDividiu a meta de economizar em 7 contas individuais para facilitar o controle.")
        st.success("**🔍 Padrões na Prática**\nSeparou contas com contratos rígidos das despesas ajustáveis.")
    with c2:
        st.warning("**🎯 Abstração na Prática**\nFocou o tempo e esforço apenas onde era possível reduzir custos.")
        st.error("**⚡ Algoritmo de Planilha**\nCriou uma rotina de 10 decisões para repetir todos os meses.")

    if st.button("🔄 REINICIAR O JOGO", type="primary"):
        st.session_state.fase = 1
        st.session_state.gastos_classificados = {}
        st.session_state.etapa_f3 = 1
        st.session_state.passos_f3 = []
        st.session_state.opcoes_shuffled = None
        st.rerun()
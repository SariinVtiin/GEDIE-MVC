-- Script alternativo usando o usuário existente "Vitor"
-- Este script NÃO altera o código de acesso, usa o existente (445376)

-- Verificar dados do usuário
SELECT 'Usuário existente:' as info;
SELECT id, telegram_id, nome, codigo_acesso, ativo 
FROM users 
WHERE telegram_id = '6212796124';

-- Obter ID do usuário
SET @user_id = (SELECT id FROM users WHERE telegram_id = '6212796124');

-- Verificar categorias existentes
SELECT 'Categorias existentes:' as info;
SELECT COUNT(*) as total_categorias 
FROM categories 
WHERE user_id = @user_id AND ativo = 1;

-- Listar categorias
SELECT id, nome, tipo, icone 
FROM categories 
WHERE user_id = @user_id AND ativo = 1;

-- Se precisar criar categorias que faltam (apenas as que não existem)
INSERT IGNORE INTO categories (nome, tipo, icone, user_id, ativo, created_at, updated_at)
SELECT * FROM (
    SELECT 'Alimentação' as nome, 'DESPESA' as tipo, '🍕' as icone, @user_id as user_id, 1 as ativo, NOW() as created_at, NOW() as updated_at
    UNION SELECT 'Transporte', 'DESPESA', '🚗', @user_id, 1, NOW(), NOW()
    UNION SELECT 'Saúde', 'DESPESA', '💊', @user_id, 1, NOW(), NOW()
    UNION SELECT 'Educação', 'DESPESA', '📚', @user_id, 1, NOW(), NOW()
    UNION SELECT 'Lazer', 'DESPESA', '🎮', @user_id, 1, NOW(), NOW()
    UNION SELECT 'Moradia', 'DESPESA', '🏠', @user_id, 1, NOW(), NOW()
    UNION SELECT 'Outros', 'DESPESA', '📦', @user_id, 1, NOW(), NOW()
) AS new_categories
WHERE NOT EXISTS (
    SELECT 1 FROM categories c 
    WHERE c.nome = new_categories.nome 
    AND c.user_id = @user_id
);

-- Verificar resultado final
SELECT 'Total de categorias após setup:' as info;
SELECT COUNT(*) as total 
FROM categories 
WHERE user_id = @user_id AND ativo = 1;

-- Limpar despesas de teste antigas (opcional)
DELETE FROM expenses 
WHERE user_id = @user_id 
AND descricao LIKE '%Despesa Teste Automatizado%';

SELECT 'Setup concluído!' as info;
SELECT CONCAT('Use o código de acesso: ', codigo_acesso) as instrucao 
FROM users 
WHERE telegram_id = '6212796124';
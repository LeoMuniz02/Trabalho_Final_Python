-- ============================================================
-- Script SQL - Sistema de Registro de Notas
-- Disciplina: Desenvolvimento Rápido de Aplicações em Python
-- ============================================================

-- 1. Criar banco de dados (execute como superusuário)
-- CREATE DATABASE registro_notas
--     WITH ENCODING 'UTF8'
--          LC_COLLATE='pt_BR.UTF-8'
--          LC_CTYPE='pt_BR.UTF-8'
--          TEMPLATE=template0;

-- 2. Conecte ao banco: \c registro_notas

-- 3. Criar tabela principal
CREATE TABLE IF NOT EXISTS alunos (
    id         SERIAL       PRIMARY KEY,
    nome       VARCHAR(150) NOT NULL,
    matricula  VARCHAR(20)  NOT NULL UNIQUE,
    disciplina VARCHAR(100) NOT NULL,
    nota1      NUMERIC(4,2) NOT NULL CHECK (nota1 BETWEEN 0 AND 10),
    nota2      NUMERIC(4,2) NOT NULL CHECK (nota2 BETWEEN 0 AND 10),
    nota3      NUMERIC(4,2) NOT NULL CHECK (nota3 BETWEEN 0 AND 10),
    criado_em  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- 4. Índices para buscas rápidas
CREATE INDEX IF NOT EXISTS idx_alunos_nome       ON alunos (nome);
CREATE INDEX IF NOT EXISTS idx_alunos_matricula  ON alunos (matricula);
CREATE INDEX IF NOT EXISTS idx_alunos_disciplina ON alunos (disciplina);

-- 5. View com média e situação calculadas
CREATE OR REPLACE VIEW vw_alunos_completo AS
SELECT
    id,
    nome,
    matricula,
    disciplina,
    nota1,
    nota2,
    nota3,
    ROUND((nota1 + nota2 + nota3) / 3.0, 2) AS media,
    CASE
        WHEN (nota1 + nota2 + nota3) / 3.0 >= 7.0 THEN 'Aprovado'
        WHEN (nota1 + nota2 + nota3) / 3.0 >= 5.0 THEN 'Recuperação'
        ELSE 'Reprovado'
    END AS situacao,
    criado_em
FROM alunos
ORDER BY nome;

-- 6. Dados de exemplo
INSERT INTO alunos (nome, matricula, disciplina, nota1, nota2, nota3)
VALUES
    ('Ana Paula Souza',      '2024001', 'Python',        8.5, 9.0, 7.5),
    ('Bruno Ferreira Lima',  '2024002', 'Python',        5.0, 6.0, 4.5),
    ('Carla Regina Matos',   '2024003', 'Python',        9.5, 8.0, 9.0),
    ('Diego Alves Costa',    '2024004', 'Banco de Dados',3.0, 4.0, 5.5),
    ('Elisa Torres Mendes',  '2024005', 'Banco de Dados',7.0, 8.5, 6.5)
ON CONFLICT (matricula) DO NOTHING;

-- 7. Verificar
SELECT * FROM vw_alunos_completo;

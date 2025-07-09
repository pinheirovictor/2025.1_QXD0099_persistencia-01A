from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Aluno(Model):
    __keyspace__ = 'escola'
    matricula = columns.Text(primary_key=True)
    nome = columns.Text(required=True)
    curso = columns.Text(required=True)
    ano = columns.Integer(required=True)

class Disciplina(Model):
    __keyspace__ = 'escola'
    codigo = columns.Text(primary_key=True)
    nome = columns.Text(required=True)
    professor = columns.Text(required=True)

class AlunoDisciplina(Model):
    __keyspace__ = 'escola'
    matricula = columns.Text(primary_key=True, partition_key=True)
    codigo_disciplina = columns.Text(primary_key=True, partition_key=False)
    # Campos extras podem ser adicionados, como ano/semestre, notas etc.

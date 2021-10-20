#Traduz os meses do inglês para o português
def months(month):
    if month == "January":
        PT_month = "Janeiro"
    
    elif month == "February":
        PT_month = "Fevereiro"
    
    elif month == "March":
        PT_month = "Março"
    
    elif month == "April":
        PT_month = "Abril"
    
    elif month == "May":
        PT_month = "Maio"
    
    elif month == "June":
        PT_month = "Junho"

    elif month == "July":
        PT_month = "Julho"

    elif month == "August":
        PT_month = "Agosto"

    elif month == "September":
        PT_month = "Setembro"

    elif month == "October":
        PT_month = "Outubro"
    
    elif month == "November":
        PT_month = "Novembro"

    elif month == "December":
        PT_month = "Dezembro"

    return PT_month



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #



#Traduz os dias da semana do inglês para o português
def days(day):

    if day == "Sunday":
        PT_day = "Domingo"
    
    elif day == "Monday":
        PT_day = "Segunda-feira"

    elif day == "Tuesday":
        PT_day = "Terça-feira"

    elif day == "Wednesday":
        PT_day = "Quarta-feira"

    elif day == "Thursday":
        PT_day = "Quinta-feira"
    
    elif day == "Friday":
        PT_day = "Sexta-feira"

    elif day == "Saturday":
        PT_day = "Sábado"

    return PT_day



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #



#Converte o nome do mês em portugues para numero
def month2num(month):
    
    if "janeiro" in month:
        month_num = '01'
    
    elif "fevereiro" in month:
        month_num = '02'
    
    elif "março" in month:
        month_num = '03'
    
    elif "abril" in month:
        month_num = '04'
    
    elif "maio" in month:
        month_num = '05'
    
    elif "junho" in month:
        month_num = '06'
    
    elif "julho" in month:
        month_num = '07'
    
    elif "agosto" in month:
        month_num = '08'
    
    elif "setembro" in month:
        month_num = '09'
    
    elif "outubro" in month:
        month_num = '10'
    
    elif "novembro" in month:
        month_num = '11'
    
    elif "dezembro" in month:
        month_num = '12'
    
    return month_num



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #


#Converte o nome do dias em portugues para a abreviação
def days_short(day):

    if "omingo" in day:
        days_short = "dom"
    
    elif "egunda" in day:
        days_short = "seg"

    elif "erça" in day:
        days_short = "ter"

    elif "uarta" in day:
        days_short = "qua"

    elif "uinta" in day:
        days_short = "qui"
    
    elif "exta" in day:
        days_short = "sex"

    elif "ábado" in day:
        days_short = "sab"

    return days_short
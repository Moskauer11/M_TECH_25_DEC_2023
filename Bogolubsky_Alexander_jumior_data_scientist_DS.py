import streamlit as st 
import pandas as pd
import scipy
import scipy.stats

st.title('           ЗАДАНИЕ ')
st.subheader('    для вакансии')
st.subheader("Младший исследователь данных (DS)")
st.subheader("Автор: Боголюбский Александр")
st.sidebar.header('Ведите параметры по вашему выбору:')

p = st.sidebar.slider('Уровень значимости:', 0.001, 0.999)
age = st.sidebar.slider('Возрастная граница:', 16, 65)

data_raw_m_video=pd.read_csv(r'c:\Users\ИОН\OneDrive\Рабочий стол\MVIDEO_TEST\М.Тех_ТЗ_DS\М.Тех_Данные_к_ТЗ_DS.csv', sep=',', encoding='cp1251', quoting=3)

new_columns=[]
for i in range(len(data_raw_m_video.columns)):
    #st.write(data_raw_m_video.columns[i])
    x=data_raw_m_video.columns[i].replace('"', "")
    #st.write(x)
    new_columns.append(x)
#st.write(new_columns)
#st.write(len(new_columns[0])
data_raw_m_video.columns=new_columns
#st.dataframe(data_raw_m_video)

new_ill_days=[]
for i in range(len(data_raw_m_video['Количество больничных дней'])):
    #st.write(data_raw_m_video['Количество больничных дней'][i])
    x=data_raw_m_video['Количество больничных дней'][i].replace('"', "")
    #st.write(x)
    new_ill_days.append(x)
#st.write(new_ill_days)
data_raw_m_video['Количество больничных дней']=new_ill_days

new_sexes=[]
for i in range(len(data_raw_m_video['Пол'])):
    #st.write(data_raw_m_video['Пол'][i])
    x=data_raw_m_video['Пол'][i].replace('"', "")
    #st.write(x)
    new_sexes.append(x)
#st.write(new_sexes)


data_raw_m_video['Пол']=new_sexes

st.subheader('----------------------------------------------------------------------')
st.subheader("Начальные данные по сотрудникам: пол, возраст, кол-во больничных дней")
st.dataframe(data_raw_m_video)


df_raw=pd.DataFrame(data_raw_m_video)
#st.dataframe(df_raw)
    
df_sexes=pd.get_dummies(df_raw, columns=['Пол'])
df_sexes['Количество больничных дней']=df_sexes['Количество больничных дней'].astype(float)
    
df_male=df_sexes[df_sexes['Пол_М']==1]
df_female=df_sexes[df_sexes['Пол_Ж']==1]
st.subheader('----------------------------------------------------------------------')
st.subheader("######################################################################")
st.subheader('----------------------------------------------------------------------')
st.subheader('Задача 1')
st.subheader('Задача о зависимости числа больничных дней от пола работника')
st.subheader('Выдвинем нулевую гипотезу - количество больничных дней больше 2-х не зависит от пола работника.')
st.write('Применим дисперсионный анализ. Применим двусторонний критерий Фишера. Обозначения: p - уровень значимости,F_sexes - значение полученной F статистики (делим var males на var females), F_crit_right - критическое значение справа, F_crit_left - критическое значение слева Если F_sexes попадает между F_crit_left и F_crit_right, то принимаем нулевую гипотезу при данном уровне значимости')

st.write('-------------------------------------------')
st.write('Подсчитаем для male и female сотрудников их число соответственно и статистику по больничным дням и mean, var и std')
sick_leaves_male_mean=df_male['Количество больничных дней'].mean()
sick_leaves_male_var=df_male['Количество больничных дней'].var()
sick_leaves_male_std=df_male['Количество больничных дней'].std()
n_males=len(df_male['Количество больничных дней'])
st.write(f'MALES: n_males={n_males},sick_leaves_male_mean={sick_leaves_male_mean:.3},sick_leaves_male_var={sick_leaves_male_var:.3},sick_leaves_male_std={sick_leaves_male_std:.3}')
sick_leaves_female_mean=df_female['Количество больничных дней'].mean()
sick_leaves_female_var=df_female['Количество больничных дней'].var()
sick_leaves_female_std=df_female['Количество больничных дней'].std()
n_females=len(df_female['Количество больничных дней'])
st.write(f'FEMALES: n_females={n_females},sick_leaves_female_mean={sick_leaves_female_mean:.3},sick_leaves_female_var={sick_leaves_female_var:.3},sick_leaves_female_std={sick_leaves_female_std:.3}')
st.write('-------------------------------------------')

F_sexes=sick_leaves_male_var/sick_leaves_female_var
F_crit_right=scipy.stats.f.ppf(1-p/2, n_males-1, n_females-1)
F_crit_left=1/(scipy.stats.f.ppf(1-p/2, n_females-1, n_males-1))
st.write("Значения полученного критерия Фишера F_sexes, критические значения критерия Фишера справа и слева F_crit_left и F_crit_right")
st.write(f'p = {p}, F_sexes={F_sexes:.3}, F_crit_left={F_crit_left:.3}, F_crit_right={F_crit_right:.3}')

st.subheader('----------------------------------------------------------------------')
st.subheader('ЗАДАЧА 1. РЕШЕНИЕ:')
st.write('----------------------------------------------------------------------')
st.subheader('НУЛЕВАЯ ГИПОТЕЗА: ЧИСЛО БОЛЬНИЧНЫХ ДНЕЙ БОЛЬШЕ 2-Х НЕ ЗАВИСИТ ОТ ПОЛА РАБОТНИКА ')
st.write('----------------------------------------------------------------------')
st.subheader('ОТВЕТ:')
if F_sexes<=F_crit_right and F_sexes>=F_crit_left:
    st.subheader(f'НУЛЕВАЯ ГИПОТЕЗА ПРИНИМАЕТСЯ при уровне значимости p={p}')
else:
    st.subheader(f'НУЛЕВАЯ ГИПОТЕЗА ОТВЕРГАЕТСЯ при уровне значимости p={p}')
st.subheader('----------------------------------------------------------------------')
st.subheader('----------------------------------------------------------------------')

st.subheader('ЗАДАЧА 2.')
st.subheader('Задача о зависимости числа больничных дней от возраста работника при выбранном граничном возраст для деления работников на две возрастные группы')
st.subheader(f'Введём граничный возраст для деления работников на группы. Выбранный возраст - {age} лет')
st.subheader(f'Разделим персонал на две группы: до выбранного возраста включительно (young) и старше выбранного возраста (old)')
df_ages=df_sexes
df_young=df_ages[df_ages['Возраст']<=age]
#st.write("Число людей, младше {age} включительно:",len(df_young))
df_old=df_ages[df_ages['Возраст']>age]
#st.write("Число людей, старше {age}:",len(df_old))
#st.write("Всего людей:",len(df_young)+len(df_old))
st.write("Выдвинем нулевую гипотезу - количество больничных дней больше 2-ч не зависит от возраста работника. Применим дисперсионный анализ. Применим двусторонний критерий Фишера. Обозначения: p - уровень значимости F_ages - значение полученной F статистики (делим var young на var old) F_crit_right - критическое значение справа F_crit_left - критическое значение слева Если F_ages попадает между F_crit_left и F_crit_right, то принимаем нулевую гипотезу при данном уровне значимости")

sick_leaves_young_mean=df_young['Количество больничных дней'].mean()
sick_leaves_young_var=df_young['Количество больничных дней'].var()
sick_leaves_young_std=df_young['Количество больничных дней'].std()
n_young=len(df_young['Количество больничных дней'])
st.write(f'Младше {age} включительно: n_young={n_young},sick_leaves_young_mean={sick_leaves_young_mean:.3},sick_leaves_young_var={sick_leaves_young_var:.3},sick_leaves_young_std={sick_leaves_young_std:.3}')

sick_leaves_old_mean=df_old['Количество больничных дней'].mean()
sick_leaves_old_var=df_old['Количество больничных дней'].var()
sick_leaves_old_std=df_old['Количество больничных дней'].std()
n_old=len(df_old['Количество больничных дней'])
st.write('Подсчитаем для old и young сотрудников их число соответственно и статистику по больничным дням и mean, var и std')
st.write(f'Старше {age} лет: n_old={n_old},sick_leaves_old_mean={sick_leaves_old_mean:.3},sick_leaves_old_var={sick_leaves_old_var:.3},sick_leaves_old_std={sick_leaves_old_std:.3}')


F_ages=sick_leaves_young_var/sick_leaves_old_var
F_crit_right=scipy.stats.f.ppf(1-p/2, n_young-1, n_old-1)
F_crit_left=1/(scipy.stats.f.ppf(1-p/2, n_old-1, n_young-1))
st.write("Значения полученного критерия Фишера F_ages, критические значения критерия Фишера справа и слева F_crit_left и F_crit_right")
st.write(f'p = {p}, F_ages={F_ages:.3}, F_crit_left={F_crit_left:.3}, F_crit_right={F_crit_right:.3}')
st.subheader("######################################################################")
st.subheader('----------------------------------------------------------------------')
st.subheader('ЗАДАЧА 2. РЕШЕНИЕ:')
print('----------------------------------------------------------------------')
st.subheader(f'НУЛЕВАЯ ГИПОТЕЗА: ЧИСЛО БОЛЬНИЧНЫХ ДНЕЙ БОЛЬШЕ 2-Х НЕ ЗАВИСИТ ОТ ВОЗРАСТА РАБОТНИКА ПРИ ВОЗРАСТЕ РАЗДЕЛЕНИЯ НА ГРУППЫ "ДО ВКЛЮЧИТЕЛЬНО" И "ПОСЛЕ" ПО ВОЗРАСТУ {age} ЛЕТ')
print('----------------------------------------------------------------------')
st.subheader('ОТВЕТ:')
if F_ages<=F_crit_right and F_ages>=F_crit_left:
    st.subheader(f'НУЛЕВАЯ ГИПОТЕЗА ПРИНИМАЕТСЯ при уровне значимости p={p}, ЧИСЛО БОЛЬНИЧНЫХ ДНЕЙ БОЛЬШЕ 2-Х НЕ ЗАВИСИТ ОТ ВОЗРАСТА РАБОТНИКА.')
else:
    st.subheader(f'НУЛЕВАЯ ГИПОТЕЗА ОТВЕРГАЕТСЯ при уровне значимости p={p}')
st.subheader('----------------------------------------------------------------------')
st.subheader("######################################################################")
st.subheader('----------------------------------------------------------------------')

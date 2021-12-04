"""Renders our page forms and views"""
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.http.request import HttpRequest
from myapp.database import *
from .forms import *
from django.http import HttpResponseRedirect
from django.core.paginator import *

"""Landing page Response Return"""
def landingpage(response):
    if response.user.is_authenticated:
        return render(response, './landingpage/landingpage.html')
    return redirect('/login')

"""if the base url is accessed redirect them to login"""
def baseUrl(response):
    return redirect('/login')

"""gathers the information for how the columns will have the animals ordered, based upon the
   order that the user selects the columns to be ordered by"""
def getOrderBy(queryParameters, orderByInfo):
    if len(queryParameters) != 0:
        for key, value in queryParameters.items():
            if key == 'common_sort':
                if value == 'asc':
                    orderByInfo += " COMMON_NAME COLLATE NOCASE ASC,"
                if value == 'desc':
                    orderByInfo += " COMMON_NAME COLLATE NOCASE DESC,"
            if key == 'scientific_sort':
                if value == 'asc':
                    orderByInfo += " SCIENTIFIC_NAME COLLATE NOCASE ASC,"
                if value == 'desc':
                    orderByInfo += " SCIENTIFIC_NAME COLLATE NOCASE DESC,"
            if key == 'region_sort':
                if value == 'asc':
                    orderByInfo += " REGION_NAME COLLATE NOCASE ASC,"
                if value == 'desc':
                    orderByInfo += " REGION_NAME COLLATE NOCASE DESC,"
            if key == 'status_sort':
                if value == 'asc':
                    orderByInfo += " STATUS_NAME COLLATE NOCASE ASC,"
                if value == 'desc':
                    orderByInfo += " STATUS_NAME COLLATE NOCASE DESC,"
            if key == 'group_sort':
                if value == 'asc':
                    orderByInfo += " GROUP_NAME COLLATE NOCASE ASC,"
                if value == 'desc':
                    orderByInfo += " GROUP_NAME COLLATE NOCASE DESC,"
    return orderByInfo

"""Updating the overall database for the page"""
def managePage(response):
    if response.user.is_authenticated:
        if response.method == "POST" and 'Create' in response.POST:
            form = AddSpeciesForm(response.POST)
            if form.is_valid():
                commonName = form.cleaned_data.get('commonName')
                scientificName = form.cleaned_data.get('scientificName')
                region = form.cleaned_data.get('region')
                conservationStatus = form.cleaned_data.get('conservationStatus')
                group = form.cleaned_data.get('group')
                newId = db_query('SELECT MAX(SPECIES_ID) FROM SPECIES')
                newId = max(newId)[0] + 1
                db_query('INSERT INTO SPECIES (SPECIES_ID, COMMON_NAME, SCIENTIFIC_NAME, REGION_ID, STATUS_ID, GROUP_ID) VALUES(%s, %s, %s, %s, %s, %s)', [newId, commonName, scientificName, region, conservationStatus, group])
                return HttpResponseRedirect(response.path_info)
        if response.method == "POST" and 'update' in response.POST:
            form = EditSpeciesForm(response.POST)
            if form.is_valid():
                sId = response.POST.get('update')
                commonName = form.cleaned_data.get("cName")
                scientificName = form.cleaned_data.get('sName')
                region = form.cleaned_data.get('reg')
                conservationStatus = form.cleaned_data.get('cStatus')
                group = form.cleaned_data.get('grp')
                db_query('UPDATE SPECIES SET COMMON_NAME =  %s, SCIENTIFIC_NAME = %s, REGION_ID = %s, STATUS_ID = %s, GROUP_ID =%s WHERE SPECIES_ID = %s', [commonName, scientificName, region, conservationStatus, group, sId])
                return HttpResponseRedirect(response.path_info)
        if response.method == "POST" and 'delete' in response.POST:
            delete_key = response.POST.get('delete')
            db_query('DELETE FROM SPECIES WHERE SPECIES_ID = %s', [delete_key])
            return HttpResponseRedirect(response.path_info)
        
        # Getting ahold of the query for species that we will run later
        species = "select species_id, common_name, scientific_name, region_name, status_name, group_name from species s,region r,species_group sg,status st where s.status_id=st.status_id and s.region_id=r.region_id and s.group_id=sg.group_id"
        speciesParam = []       
        #species = db_query("select species_id, common_name, scientific_name, region_name, status_name, group_name from species s,region r,species_group sg,status st where s.status_id=st.status_id and s.region_id=r.region_id and s.group_id=sg.group_id")

        # Statement used for filtering
        if response.method == "GET" and 'filterTextBox' in response.GET:
            # The first part of the statement is necessary b/c it is the default query
            if "fCName" in response.GET and response.GET['fCName'] != "":
                filterCName = response.GET['fCName']
                # Must have percent sign BEFORE and AFTER the word they are attempting to search (Pattern Matching)
                filterCName_PM = "%" + filterCName + "%"
                species += " and common_name like %s"
                speciesParam.append(filterCName_PM)
            if "fSName" in response.GET and response.GET['fSName'] != "":
                filterSName = response.GET['fSName']
                # Must have percent sign BEFORE and AFTER the word they are attempting to search (Pattern Matching)
                filterSName_PM = "%" + filterSName + "%"
                species += " and scientific_name like %s"
                speciesParam.append(filterSName_PM)
            if "fReg" in response.GET and response.GET['fReg'] != '0':
                filterReg = response.GET['fReg']
                species += " and s.region_id = %s"
                speciesParam.append(int(filterReg))
            if "fCStatus" in response.GET and response.GET['fCStatus'] != '0':
                filterCStatus = response.GET['fCStatus']
                species += " and s.status_id = %s"
                speciesParam.append(int(filterCStatus))
            if "fGrp" in response.GET and response.GET['fGrp'] != '0':
                filterGrp = response.GET['fGrp']
                species += " and s.group_id = %s"
                speciesParam.append(int(filterGrp))
            
        # Update this for OrderBy statement to allow ordering based on the URL
        # and if it is in asc or desc order
        orderByInfo = " ORDER BY"
        # Call the function to get the orderBY information
        orderByInfo = getOrderBy(response.GET.copy(), orderByInfo)

        # The length before the GROUP BY is 9, so if you have something that is being grouped for 
        # asc or desc order
        if len(orderByInfo) > 9:
            # Cut off the last comma
            orderByInfo = orderByInfo[0: len(orderByInfo) - 1]
            # Append the orderBy info to the species
            species = species + orderByInfo

        # The forms with the functions are below
        form = AddSpeciesForm()
        form2 = EditSpeciesForm()
        form3 = FilterSpeciesForm()

        # The query that may have been updated previously in the function
        speciesData = db_query(species, speciesParam)

        # Info for a paginator with the data of the species with pages included
        p = Paginator(speciesData,50)
        page_number = 1
        if "page" in response.GET:
            page_number = response.GET['page']
        speciesPaginate = p.get_page(page_number)

        context = {
            'speciesPaginate': speciesPaginate,
            'form': form,
            'form2': form2,
            'form3': form3
        }
        return render(response,'./manage/manage.html',context)
    return redirect('/login')

"""For the education page, contains the list of species"""
def educationList(response):
    if response.user.is_authenticated:
        mammalsQuery = "select species_id, common_name, scientific_name, region_name, status_name, group_name from species s,region r,species_group sg,status st where s.status_id=st.status_id and s.region_id=r.region_id and s.group_id=sg.group_id and sg.group_name = 'Mammals'"
        mammalsParams = []
        if response.method == "GET" and 'filterTextBox' in response.GET:
            fCName = response.GET['fCommonName']
            fCName = "%" + fCName + "%"
            mammalsQuery += "and common_name like %s"
            mammalsParams.append(fCName)

            fSName = response.GET['fScientificName']
            fSName = "%" + fSName + "%"
            mammalsQuery += "and scientific_name like %s"
            mammalsParams.append(fSName)

            if "fRegion" in response.GET and response.GET['fRegion'] != '0':
                fReg = response.GET['fRegion']
                mammalsQuery += 'and s.region_id = %s'
                mammalsParams.append(int(fReg))
            if "fConservationStatus" in response.GET and response.GET['fConservationStatus'] != '0':
                fCStatus = response.GET['fConservationStatus']
                mammalsQuery += 'and s.status_id = %s'
                mammalsParams.append(int(fCStatus))
        
        # Update this for OrderBy statement to allow ordering based on the URL
        # and if it is in asc or desc order
        orderByInfo = " ORDER BY"
        # Call the function to get the orderBY information
        orderByInfo = getOrderBy(response.GET.copy(), orderByInfo)

        filterListForm = FilterEducationListForm()

        # The length before the GROUP BY is 9, so if you have something that is being grouped for 
        # asc or desc order
        if len(orderByInfo) > 9:
            # Cut off the last comma
            orderByInfo = orderByInfo[0: len(orderByInfo) - 1]
            # Append the orderBy info to the species
            mammalsQuery += orderByInfo

        mammalsData = db_query(mammalsQuery, mammalsParams)
        #p = Paginator(mammals,50)
        #page_number = 1
        #if "page" in response.GET:
        #   page_number = response.GET['page']
        #educatePaginate = p.get_page(page_number)
        context = {
        #   'educatePaginate': educatePaginate,
            'filterListForm': filterListForm,
            'mammals': mammalsData
        }
        return render(response, './education/educationList.html', context)
    return redirect('/login')

"""Information to update/change the region page"""
def manageRegion(response):
    if response.user.is_authenticated:
        if response.method == "POST" and 'Create' in response.POST:
            form = AddRegionForm(response.POST)
            if form.is_valid():
                region = form.cleaned_data.get('region')
                existingRegion = db_query('SELECT REGION_NAME FROM REGION WHERE REGION_NAME = %s COLLATE NOCASE', [region])
                if existingRegion == []:
                    newId = db_query('SELECT MAX(REGION_ID) FROM REGION')
                    newId = max(newId)[0] + 1
                    db_query('INSERT INTO REGION (REGION_ID, REGION_NAME, DELETED) VALUES(%s, %s, %s)', [newId, region, 0])
                else:
                    db_query('UPDATE REGION SET DELETED = %s WHERE REGION_NAME = %s COLLATE NOCASE', [0, region])
                return HttpResponseRedirect(response.path_info)
        if response.method == "POST" and 'update' in response.POST:
            form = EditRegionForm(response.POST)
            if form.is_valid():
                regionName = form.cleaned_data.get('reg')
                regionId = response.POST.get('update')
                db_query('UPDATE REGION SET REGION_NAME = %s WHERE REGION_ID = %s', [regionName, regionId])
                return HttpResponseRedirect(response.path_info)
        if response.method == "POST" and 'delete' in response.POST:
            delete_key = response.POST.get('delete')
            db_query('UPDATE REGION SET DELETED = %s WHERE REGION_ID = %s', [1, delete_key])
            return HttpResponseRedirect(response.path_info)

        regions = 'SELECT * FROM REGION WHERE DELETED = 0'
        regionParam = []

        if response.method == "GET" and 'filterTextBox' in response.GET:
            fReg = response.GET['fRegion']
            fReg = "%" + fReg + "%"
            regions += " AND REGION_NAME LIKE %s"
            regionParam.append(fReg)

        # Update this for OrderBy statement to allow ordering based on the URL
        # and if it is in asc or desc order
        orderByInfo = " ORDER BY"
        # Call the function to get the orderBY information
        orderByInfo = getOrderBy(response.GET.copy(), orderByInfo)

        if len(orderByInfo) > 9:
            # Cut off the last comma
            orderByInfo = orderByInfo[0: len(orderByInfo) - 1]
            # Append the orderBy info to the species
            regions += orderByInfo   

        regions = db_query(regions, regionParam)

        form = AddRegionForm()
        form2 = EditRegionForm()
        filterRegion = FilterRegionForm()

        context = {
            'regions': regions,
            'form': form,
            'form2': form2,
            'filterRegion': filterRegion
        }
        return render(response, './manage/manageregions.html', context)
    return redirect('/login')

"""Information to update/change the group page"""
def manageGroups(response):
    if response.user.is_authenticated:
        if response.method == "POST" and 'Create' in response.POST:
            form = AddGroupForm(response.POST)
            if form.is_valid():
                group = form.cleaned_data.get('group')
                existingGroup = db_query('SELECT GROUP_NAME FROM SPECIES_GROUP WHERE GROUP_NAME = %s COLLATE NOCASE', [group])
                if existingGroup == []:
                    print('here')
                    newId = db_query("SELECT MAX(GROUP_ID) FROM SPECIES_GROUP")
                    newId = max(newId)[0] + 1
                    db_query('INSERT INTO SPECIES_GROUP (GROUP_ID, GROUP_NAME, DELETED) VALUES(%s, %s, %s)', [newId, group, 0])
                else:
                    db_query('UPDATE SPECIES_GROUP SET DELETED = %s WHERE GROUP_NAME = %s COLLATE NOCASE', [0, group])
                return HttpResponseRedirect(response.path_info)
        if response.method == "POST" and 'delete' in response.POST:
            delete_key = response.POST.get('delete')
            db_query('UPDATE SPECIES_GROUP SET DELETED = %s WHERE GROUP_ID = %s', [1, delete_key])
            return HttpResponseRedirect(response.path_info)
        if response.method == "POST" and 'update' in response.POST:
            form = EditGroupForm(response.POST)
            if form.is_valid():
                groupName = form.cleaned_data.get('grp')
                groupId = response.POST.get('update')
                db_query('UPDATE SPECIES_GROUP SET GROUP_NAME = %s WHERE GROUP_ID = %s', [groupName, groupId])
                return HttpResponseRedirect(response.path_info)
        
        groups = 'SELECT * FROM SPECIES_GROUP WHERE DELETED = 0'
        groupParam = []

        if response.method == "GET" and 'filterTextBox' in response.GET:
            fGrp = response.GET['fGroup']
            fGrp = "%" + fGrp + "%"
            groups += ' AND GROUP_NAME LIKE %s'
            groupParam.append(fGrp)

        # Update this for OrderBy statement to allow ordering based on the URL
        # and if it is in asc or desc order
        orderByInfo = " ORDER BY"
        # Call the function to get the orderBY information
        orderByInfo = getOrderBy(response.GET.copy(), orderByInfo)

        if len(orderByInfo) > 9:
            # Cut off the last comma
            orderByInfo = orderByInfo[0: len(orderByInfo) - 1]
            # Append the orderBy info to the species
            groups += orderByInfo   
             
        groups = db_query(groups, groupParam)

        form = AddGroupForm()
        form2 = EditGroupForm()
        filterGroup = FilterGroupForm()

        context = {
            'groups': groups,
            'form': form,
            'form2': form2,
            'filterGroup': filterGroup
        }
        return render(response, './manage/managegroups.html', context)
    return redirect('/login')

"""Information to update/change the status page"""
def manageStatuses(response):
    if response.user.is_authenticated:
        if response.method == "POST" and 'Create' in response.POST:
            form = AddCStatusForm(response.POST)
            if form.is_valid():
                status = form.cleaned_data.get('status')
                existingStatus = db_query('SELECT STATUS_NAME FROM STATUS WHERE STATUS_NAME = lower(%s) COLLATE NOCASE', [status])
                if existingStatus == []:
                    newId = db_query('SELECT MAX(STATUS_ID) FROM STATUS')
                    newId = max(newId)[0] + 1
                    db_query('INSERT INTO STATUS (STATUS_ID, STATUS_NAME, DELETED) VALUES(%s, %s, %s)', [newId, status, 0])
                else:
                    db_query('UPDATE STATUS SET DELETED = %s WHERE STATUS_NAME = %s COLLATE NOCASE', [0, status])
                return HttpResponseRedirect(response.path_info)
        if response.method == "POST" and 'delete' in response.POST:
            delete_key = response.POST.get('delete')
            db_query('UPDATE STATUS SET DELETED = %s WHERE STATUS_ID = %s', [1, delete_key])
            return HttpResponseRedirect(response.path_info)

        if response.method == "POST" and 'update' in response.POST:
            print("here")
            form = EditCStatusForm(response.POST)
            if form.is_valid():
                statusName = form.cleaned_data.get('stat')
                statusId = response.POST.get('update')
                db_query('UPDATE STATUS SET STATUS_NAME = %s WHERE STATUS_ID = %s', [statusName, statusId])
                return HttpResponseRedirect(response.path_info)

        status = 'SELECT * FROM STATUS WHERE DELETED = 0'
        statusParam = []

        if response.method == "GET" and 'filterTextBox' in response.GET:
            fStat = response.GET['fStatus']
            fStat = "%" + fStat + "%"
            status += ' AND STATUS_NAME LIKE %s'
            statusParam.append(fStat)
    
        # Update this for OrderBy statement to allow ordering based on the URL
        # and if it is in asc or desc order
        orderByInfo = " ORDER BY"
        # Call the function to get the orderBY information
        orderByInfo = getOrderBy(response.GET.copy(), orderByInfo)

        if len(orderByInfo) > 9:
            # Cut off the last comma
            orderByInfo = orderByInfo[0: len(orderByInfo) - 1]
            # Append the orderBy info to the species
            status += orderByInfo   
             
        status = db_query(status, statusParam)

        form = AddCStatusForm()
        form2 = EditCStatusForm()
        filterStatus = FilterStatusForm()

        context = {
            'status': status,
            'form': form,
            'form2': form2,
            'filterStatus': filterStatus
        }
        return render(response, './manage/managestatuses.html', context)
    return redirect('/login')
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def mammalPage(response):
    if response.user.is_authenticated:
        mammalId = response.GET.copy()['id']
        status = db_query('SELECT STATUS_ID FROM SPECIES WHERE SPECIES_ID = %s', [mammalId])
        status = max(status[0])
        image = db_query('SELECT IMAGE FROM EDUCATION_IMAGE WHERE SPECIES_ID = %s', [mammalId])
        empPhoto = convertToBinaryData(image)
        print(empPhoto)
        mammal = db_query('SELECT COMMON_NAME, SCIENTIFIC_NAME, STATUS_NAME, IMAGE, URL FROM EDUCATION_URL AS U, SPECIES AS S, STATUS AS SG, EDUCATION_IMAGE AS EI WHERE U.SPECIES_ID = %s AND S.SPECIES_ID = %s AND SG.STATUS_ID = %s AND EI.SPECIES_ID = %s', [mammalId, mammalId, status, mammalId])
        context = {
            'mammal': mammal
        }
        return render(response, './education/mammals.html', context)
    return redirect('/login')
